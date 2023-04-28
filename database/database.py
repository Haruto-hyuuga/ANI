import pymongo, os
from config import DB_URI


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["CHAT"]


user_data = database['Users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    if not await present_user(user_id):
        user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return


chat_data = database['GROUPs']

async def present_chat(chat_id: int):
    found = chat_data.find_one({'_id': chat_id})
    return bool(found)

async def add_chat(chat_id: int):
    if not await present_chat(chat_id):
        chat_data.insert_one({'_id': chat_id})
    return

async def full_chatbase():
    chat_docs = chat_data.find()
    chat_ids = []
    for doc in chat_docs:
        chat_ids.append(doc['_id'])
    return chat_ids

async def del_chat(chat_id: int):
    chat_data.delete_one({'_id': chat_id})
    return
