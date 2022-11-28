from bson import ObjectId


def convert_to_object_id(id):
    if type(id) == str:
        return ObjectId(id)
    return id


