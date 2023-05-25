from bson import DBRef
from bson.objectid import ObjectId
from typing import Generic, TypeVar, get_args, List
from main import db

T = TypeVar("T")


class AbstractRepository(Generic[T]):
    def __init__(self):
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower()

    def save(self, item: T):
        laColeccion = db[self.coleccion]
        elId = ""
        item = self.transformRefs(item)
        print("acá estoy")
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            print(elId)
            _id = ObjectId(elId)
            laColeccion = db[self.coleccion]
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
        laColeccion = db[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = db[self.coleccion]
        if hasattr(item, '_id'):
            delattr(item, '_id')
        if not isinstance(item, dict):
            item = item.__dict__
        updateItem = {"$set": {key: value for key,
                               value in item.items() if key != '_id'}}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    def updateArray(self, id, array, obj):
        laColeccion = db[self.coleccion]
        _id_collection = ObjectId(id)
        _id_array = ObjectId(obj._id)
        element_class = str(obj.__class__.__name__.lower())
        x = laColeccion.update_one({"_id": _id_collection}, {
                                   '$push': {array: {'collection': element_class, '_id': _id_array}}})
        return {"updated_count": x.matched_count}

    def deleteFromArray(self, id, array, obj):
        laColeccion = db[self.coleccion]
        _id_collection = ObjectId(id)
        _id_array = ObjectId(obj._id)
        element_class = str(obj.__class__.__name__.lower())
        x = laColeccion.update_one({"_id": _id_collection}, {
            '$pull': {array: {'collection': element_class, '_id': _id_array}}})
        return {"updated_count": x.matched_count}

    def findById(self, id, laColeccion=None):
        if laColeccion == None:
            laColeccion = db[self.coleccion]
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
        laColeccion = db[self.coleccion]
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

    def findAll(self):
        laColeccion = db[self.coleccion]

        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)

            x = self.replaceDBRefsWithObjects(x)
            data.append(x)

        return data

    def query(self, theQuery):
        laColeccion = db[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        return data

    def queryAggregation(self, theQuery):
        laColeccion = db[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):

                laColeccion = db[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                print("valor cadena", x[k])
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
        laColeccion = db[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def transformObjectIds(self, x):
        for attribute in x.keys():
            #print('atribute', x[attribute], "type", type(x[attribute]))
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
                        result = self.findById(obj_id, db[ref_collection])
                        modified_obj[key][i] = result
            if isinstance(modified_obj[key], dict) and ("collection" in modified_obj[key]
                                                        and "_id" in modified_obj[key]):
                ref_collection = modified_obj[key]["collection"]
                obj_id = modified_obj[key]["_id"]
                result = self.findById(str(obj_id), db[ref_collection])
                print("result", result)
                modified_obj[key] = result
        return modified_obj
