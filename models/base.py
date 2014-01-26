# Models and Collections (abstract classes)
# Models represent individual entries in a database, while Collections
# represent entire collections in a databse
from pymongo import MongoClient
from gridfs import GridFS
from datetime import datetime
from settings import DB_NAME, COLLECTIONS, IGNORE_ATTRS


class Model(object):

    def __init__(self, db, fs, collection, obj=None):
        for key in obj:
            self.__dict__[key] = obj[key]
        self.db = db
        self.collection = collection
        self.fs = fs
        self._obj = obj

    # Gets _id
    def get_id(self):
        return self._id

    # Gets the date converted to a string
    def get_date_string(self):
        return self.date.strftime('%A, %B %d')

    # Perform an update
    def save(self):
        for key in self.__dict__:
            if key not in IGNORE_ATTRS:
                self._obj[key] = self.__dict__[key]
        self.collection.objects.update({'_id': self.get_id()}, self._obj)

    # Removes the object from database
    def remove(self):
        self.objects.remove({'_id': self._id})


class Collection(object):

    def __init__(self, model=Model):
        client = MongoClient()
        self.db = client[DB_NAME]
        self.fs = GridFS(self.db)
        self.objects = self.db[COLLECTIONS[self.__class__.__name__]]
        self.name = COLLECTIONS[self.__class__.__name__]
        self.model = model

    # Converts list of dict objects to Model objects
    def to_objects(self, objs):
        model = self.model
        if objs:
            return [model(self.db, self.fs, self, o) for o in objs]
        return None

    # Returns a model list corresponding to find in database
    def find(self, **kwargs):
        return self.to_objects(self.objects.find(kwargs))

    # Returns a model object corresponding to find_one in database
    def find_one(self, **kwargs):
        model = self.model
        obj = self.objects.find_one(kwargs)
        if obj:
            return model(self.db, self.fs, self, obj)
        return None

    # Inserts objects into collection
    def insert(self, **kwargs):
        kwargs['date'] = datetime.now()
        id = self.objects.insert(kwargs)
        return self.find_one(_id=id)

    # Remove all objects in the collection
    def remove_all(self):
        self.objects.remove()

    # Remove objects based on keyword parameters
    def remove(self, **kwargs):
        self.objects.remove(kwargs)

    # Return model objects forted by certain values
    def sort_by(self, sort_vals, **kwargs):
        return self.to_objects(self.objects.find(kwargs).sort(sort_vals))

    # Gets anything by date
    def get_by_date(self, **kwargs):
        return self.sort_by([('date', -1)], **kwargs)
