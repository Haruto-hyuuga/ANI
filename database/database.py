import pymongo, os
from config import DB_URI


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["CHAT"]


user_data = database['Users']
gc_data = database['Groups']


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
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



async def present_group(group_id : int):
    found = gc_data.find_one({'_id': group_id})
    return bool(found)

async def add_group(group_id: int):
    user_data.insert_one({'_id': group_id})
    return

async def full_group():
    user_docs = gc_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_group(group_id: int):
    gc_data.delete_one({'_id': group_id})
    return
