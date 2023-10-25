from bson import ObjectId
from bson.json_util import default

def json_encoder_mongo(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return default(obj)