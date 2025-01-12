import math
from bson import DBRef
from bson.objectid import ObjectId
from typing import Generic, TypeVar, get_args
from app.config.database import Database
from typing import List


T = TypeVar("T")


class AbstractRepository(Generic[T]):
    _db = Database()

    def __init__(self):
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower()
        self.db = self._db.connect()

    def save(self, item: T):
        laColeccion = self.db[self.coleccion]
        elId = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion = self.db[self.coleccion]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()

        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()

        return self.findById(elId)
    def delete(self, id):
        laColeccion = self.db[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    def deleteByField(self, field_name, field_value):
        laColeccion = self.db[self.coleccion]
        query = {field_name: field_value}
        result = laColeccion.delete_one(query)
        deleted_count = result.deleted_count
        return {"deleted_count": deleted_count}

    def deleteAllByField(self, field_name, field_value):
        laColeccion = self.db[self.coleccion]
        query = {field_name: field_value}
        result = laColeccion.delete_many(query)
        deleted_count = result.deleted_count
        return {"deleted_count": deleted_count}

    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.db[self.coleccion]
        if hasattr(item, '_id'):
            delattr(item, '_id')
        if not isinstance(item, dict):
            item = item.__dict__
        updateItem = {"$set": {key: value for key,
                               value in item.items() if key != '_id'}}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    def updateArray(self, id, array, obj):
        laColeccion = self.db[self.coleccion]
        _id_collection = ObjectId(id)
        _id_array = ObjectId(obj._id)
        element_class = str(obj.__class__.__name__.lower())
        x = laColeccion.update_one({"_id": _id_collection}, {
                                   '$push': {array: {'collection': element_class, '_id': _id_array}}})
        return {"updated_count": x.matched_count}

    def deleteFromArray(self, id, array, obj):
        laColeccion = self.db[self.coleccion]
        _id_collection = ObjectId(id)
        _id_array = ObjectId(obj._id)
        element_class = str(obj.__class__.__name__.lower())
        x = laColeccion.update_one({"_id": _id_collection}, {
            '$pull': {array: {'collection': element_class, '_id': _id_array}}})
        return {"updated_count": x.matched_count}

    def deleteFromArrayMany(self, id, array, laColeccion=None):
        if laColeccion == None:
            laColeccion = self.db[self.coleccion]
        else:
            laColeccion = self.db[laColeccion]
        query = {array[1] + "._id": ObjectId(id)}
        update = {"$pull": {array[1]: {"_id": ObjectId(id)}}}
        x = laColeccion.update_many(query, update)

    def findById(self, id, laColeccion=None):
        if laColeccion == None:
            laColeccion = self.db[self.coleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        if x != None:
            x = self.replaceDBRefsWithObjects(x)
        else:
            return x
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def findByField(self, field, field_value):
        laColeccion = self.db[self.coleccion]
        x = laColeccion.find_one({field: field_value})
        if x != None:
            x = self.replaceDBRefsWithObjects(x)
        else:
            return x
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def findAllByField(self, field, field_value, page=None, limit=None):
        laColeccion = self.db[self.coleccion]
        query = {field: field_value}
        total_documents = laColeccion.count_documents(query)
        total_pages = None
        data = []

        if page is not None and limit is not None:
            skip = (page - 1) * limit
            cursor = laColeccion.find(query).skip(skip).limit(limit)
            total_pages = int(math.ceil(total_documents / limit))
        else:
            cursor = laColeccion.find(query)
        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        if total_pages != None:
            return {"data": data, "totalPages": total_pages}
        else:
            return data

    def findAll(self, page=None, limit=None):
        laColeccion = self.db[self.coleccion]
        total_documents = laColeccion.count_documents({})
        total_pages = None
        data = []
        if page is not None and limit is not None:
            skip = (page - 1) * limit
            cursor = laColeccion.find().skip(skip).limit(limit)
            total_pages = int(math.ceil(total_documents / limit))
        else:
            cursor = laColeccion.find()
        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        if total_pages != None:
            return {"data": data, "totalPages": total_pages}
        else:
            return data

    def existsByField(self, field, field_value):
        laColeccion = self.db[self.coleccion]
        query = {field: field_value}
        count = laColeccion.count_documents(query)
        return count > 0

    def sort(self, field, order):
        laColeccion = self.db[self.coleccion]
        data = []
        for x in laColeccion.find().sort(field, order):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        return data

    def query(self, theQuery, page=None, limit=None):
        laColeccion = self.db[self.coleccion]
        total_documents = laColeccion.count_documents(theQuery)
        total_pages = None
        data = []
        if page is not None and limit is not None:
            skip = (page - 1) * limit
            cursor = laColeccion.find(theQuery).skip(skip).limit(limit)
            total_pages = int(math.ceil(total_documents / limit))
        else:
            cursor = laColeccion.find(theQuery)

        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        if total_pages != None:
            return {"data": data, "totalPages": total_pages}
        else:
            return data

    def queryAggregation(self, theQuery):
        laColeccion = self.db[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            if '_id' in x:
                x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        return data

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):

                laColeccion = self.db[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict):
                x[k] = self.getValuesDBRef(x[k])
        return x

    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.db[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def transformObjectIds(self, x):
        for attribute in x.keys():
            # print('atribute', x[attribute], "type", type(x[attribute]))
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute] = self.transformObjectIds(x[attribute])
        return x

    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList

    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))

    def replaceDBRefsWithObjects(self, obj):
        modified_obj = obj.copy()
        for key in modified_obj:
            if isinstance(modified_obj[key], list):
                for i in range(len(modified_obj[key])):
                    if isinstance(modified_obj[key][i], dict) and "collection" in modified_obj[key][i] \
                            and "_id" in modified_obj[key][i]:
                        ref_collection = modified_obj[key][i]["collection"]
                        obj_id = modified_obj[key][i]["_id"]
                        # Search the entire object in the database
                        result = self.findById(obj_id, self.db[ref_collection])
                        modified_obj[key][i] = result
            if isinstance(modified_obj[key], dict) and ("collection" in modified_obj[key]
                                                        and "_id" in modified_obj[key]):
                ref_collection = modified_obj[key]["collection"]
                obj_id = modified_obj[key]["_id"]
                result = self.findById(str(obj_id), self.db[ref_collection])
                modified_obj[key] = result
        return modified_obj

    def insertMany(self, items: List[T]) -> None:
        laColeccion = self.db[self.coleccion]
        documents = [item.__dict__ for item in items]
        result = laColeccion.insert_many(documents)
        return result.acknowledged

    def count(self, query=None):
        laColeccion = self.db[self.coleccion]
        if query:
            return laColeccion.count_documents(query)
        else:
            return laColeccion.count_documents({})
