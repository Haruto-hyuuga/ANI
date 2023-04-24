import pymongo, os
from config import USER_STATS_DB

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["BOT_USERS"]

User_S = database['USER_STATS']

async def present_user_stats(user_id : int):
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
    if not await present_user_stats(UID):
        try:
            await add_user_stats(UID)
            User_S.update_one({'_id': user_id}, {'$inc': {'_DL': 1}}, upsert=True)
        except:
            pass
    else:
        User_S.update_one({'_id': user_id}, {'$inc': {'_DL': 1}}, upsert=True)
        
    return

async def update_RQ(user_id: int):
    if not await present_user_stats(UID):
        try:
            await add_user_stats(UID)
            User_S.update_one({'_id': user_id}, {'$inc': {'_RQ': 1}}, upsert=True)
        except:
            pass
    else:
        User_S.update_one({'_id': user_id}, {'$inc': {'_RQ': 1}}, upsert=True)
    
    return

async def update_SC(user_id: int):
    if not await present_user_stats(UID):
        try:
            await add_user_stats(UID)
            User_S.update_one({'_id': user_id}, {'$inc': {'_SrCh': 1}}, upsert=True)
        except:
            pass
    else:
        User_S.update_one({'_id': user_id}, {'$inc': {'_SrCh': 1}}, upsert=True)
        
    return

async def update_Anid(user_id: int, Ani_UID: str):
    if not await present_user_stats(UID):
        try:
            await add_user_stats(UID)
            User_S.update_one({'_id': user_id}, {'$set': {'Ani_id': Ani_UID}}, upsert=True)
        except:
            pass
    else:
        User_S.update_one({'_id': user_id}, {'$set': {'Ani_id': Ani_UID}}, upsert=True)
        
    return

async def get_user_stats(user_id: int):
    user_stats = User_S.find_one({'_id': user_id})
    D_L = user_stats['_DL']
    R_Q = user_stats['_RQ']
    S_R = user_stats['_SrCh']
    Ani_i = user_stats['Ani_id']
    return D_L, R_Q, S_R, Ani_i

async def full_stats_userbase():
    user_docs = User_S.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user_stats(user_id: int):
    User_S.delete_one({'_id': user_id})
    return
