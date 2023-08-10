from bson import ObjectId


def extract_objects_dict(object, object_array, collection):
    obj_list = object[object_array]
    objs_dict = []
    for obj in obj_list:
        obj_dict = {
            "collection": collection,
            "_id": ObjectId(obj["_id"]),
        }
        print(obj_dict)
        objs_dict.append(obj_dict)
    return objs_dict


def extract_object_dict(object, item, collection):
    object_item = object[item]
    obj_dict = {
        "collection": collection,
        "_id": ObjectId(object_item["_id"]),
    }
    return obj_dict
