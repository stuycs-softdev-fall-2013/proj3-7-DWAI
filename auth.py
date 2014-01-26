from pymongo import MongoClient
client = MongoClient()
db = client.database

def adduser(username, password):
        u = db.login.find_one({'username':username})
        if u is None:
                db.login.insert({'username':username,'password':password})
                return True
        return False

def authenticate(username, password):
        u = db.login.find_one({'username':username})
        if u is None:
                return False
        return u['password'] == password

def changepass(username, old, new):
        if authenticate(username, old):
                db.login.update({'username':username}, {'$set':{'password':new}})
                return True
	return False

def changeuser(password, old, new):
	if authenticate(old, password):
		db.login.update({'username':old}, {'$set':{'username':new}})
		return True
	return False
