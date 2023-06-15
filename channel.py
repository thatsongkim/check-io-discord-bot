import pymongo

host = "localhost"
port = 27017
client = pymongo.MongoClient(host, port)


def set_voice_channel(guild_id: int, voice_channel_id: int):
    db = client["discord"]
    collection = db["channels"]
    collection.update_one({"guild_id": guild_id},
                          {"$set": {"voice_channel_id": voice_channel_id}},
                          upsert=True)


def set_message_channel(guild_id: int, message_channel_id: int):
    db = client["discord"]
    collection = db["channels"]
    collection.update_one({"guild_id": guild_id},
                          {"$set": {"message_channel_id": message_channel_id}},
                          upsert=True)


def get_channels(guild_id: int):
    db = client["discord"]
    collection = db["channels"]
    return collection.find_one({"guild_id": guild_id})
