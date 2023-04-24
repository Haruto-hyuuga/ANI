import pymongo, os
from config import USER_STATS_DB

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["BOT_USERS"]

User_S = database['USER_STATS']

async def present_user(user_id : int):
    found = User_S.find_one({'_id': user_id})
    return bool(found)

async def add_user_stats(user_id: int):
    User_S.insert_one(
      {
        '_id': user_id,
        '_DL': 0
        '_RQ': 0
        '_SrCh': 0
        'Ani_id': 0
      }
    )
    return

async def update_DL(user_id: int):
async def add_user_stats(user_id: int):
    User_S.update_one({'_id': user_id}, {'$inc': {'_DL': 1}}, upsert=True)
    return


async def full_userbase_stats():
    user_docs = User_S.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user_stats(user_id: int):
    User_S.delete_one({'_id': user_id})
    return
