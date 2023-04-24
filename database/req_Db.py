import pymongo, os
from config import USER_STATS_DB


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient["REQUESTS"]


Req_Sub = database['Sub_Anime']

async def present_SUB_request(anime_id: int):
    found = Req_Sub.find_one({'_id': anime_id})
    return bool(found)

async def add_SUB_request(anime_id: int):
    Req_Sub.insert_one({'_id': anime_id})
    return

async def full_requestDB_SUB():
    user_docs = Req_Sub.find()
    anime_id = []
    for doc in user_docs:
        anime_id.append(doc['_id'])
        
    return anime_id

async def del_SUB_request(anime_id: int):
    Req_Sub.delete_one({'_id': anime_id})
    return



Req_Dub = database['Dub_Anime']

async def present_DUB_request(anime_id: int):
    found = Req_Dub.find_one({'_id': anime_id})
    return bool(found)

async def add_DUB_request(anime_id: int):
    Req_Dub.insert_one({'_id': anime_id})
    return

async def full_requestDB_DUB():
    user_docs = Req_Dub.find()
    anime_id = []
    for doc in user_docs:
        anime_id.append(doc['_id'])
        
    return anime_id

async def del_DUB_request(anime_id: int):
    Req_Dub.delete_one({'_id': anime_id})
    return
