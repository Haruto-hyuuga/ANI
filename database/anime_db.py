import pymongo, os
from config import SUB_ANIME_DB, DUB_ANIME_DB

dbclient1 = pymongo.MongoClient(SUB_ANIME_DB)
database1 = dbclient1["SUB_ANIME"]
sub_anime = database1['Anime_list']

dbclient2 = pymongo.MongoClient(DUB_ANIME_DB)
database2 = dbclient2["DUB_ANIME"]
dub_anime = database2['Anime_list']

async def present_sub_anime(anime_id : int):
    found = sub_anime.find_one({'_id': anime_id})
    return bool(found)

async def add_sub_anime(anime_id: int, link: str):
    sub_anime.insert_one({'_id': anime_id, '_link': link})
    return

async def full_sub_Animebase():
    user_docs = sub_anime.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_sub_anime(anime_id: int):
    sub_anime.delete_one({'_id': anime_id})
    return

async def get_sub_anime(anime_id : int):
    found = sub_anime.find_one({'_id': anime_id})
    sblink = found['_link']
    return sblink
###################################################################################

async def present_dub_anime(anime_id : int):
    found = dub_anime.find_one({'_id': anime_id})
    return bool(found)

async def add_dub_anime(anime_id: int, link: str):
    dub_anime.insert_one({'_id': anime_id, '_link': link})
    return

async def full_dub_Animebase():
    user_docs = dub_anime.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_dub_anime(anime_id: int):
    dub_anime.delete_one({'_id': anime_id})
    return

async def get_dub_anime(anime_id : int):
    found = dub_anime.find_one({'_id': anime_id})
    dblink = found['_link']
    return dblink
###################################################################################

import random

async def recom_ani_id():
    try:
        S = sub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        S_I = S['_id']
        D = dub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        D_I = D['_id']
        AniId = random.choice([S_I, D_I])
    except Exception as e:
        print(e)
    return AniId

async def recom_SUB_id():
    try:
        S1 = sub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        S1_I = S1['_id']
        S2 = sub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        S2_I = S2['_id']
        AniId = random.choice([S1_I, S2_I])
    except Exception as e:
        print(e)
    return AniId

async def recom_DUB_id():
    try:
        D1 = dub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        D1_I = D1['_id']
        D2 = dub_anime.aggregate([{"$sample": {"size": 1}}]).next()
        D2_I = D2['_id']
        AniId = random.choice([D1_I, D2_I])
    except Exception as e:
        print(e)
    return AniId
