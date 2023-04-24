import pymongo, os
from config import USER_STATS_DB


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["REQUESTS"]


Req_data = database['anime']

async def present_request(anime_id: int):
    found = Req_data.find_one({'_id': anime_id})
    return bool(found)

async def add_request(anime_id: int):
    Req_data.insert_one({'_id': anime_id})
    return

async def full_requestDB():
    user_docs = Req_data.find()
    anime_id = []
    for doc in user_docs:
        anime_id.append(doc['_id'])
        
    return anime_id

async def del_request(anime_id: int):
    Req_data.delete_one({'_id': anime_id})
    return
