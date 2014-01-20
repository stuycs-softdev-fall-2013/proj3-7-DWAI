from pymongo import MongoClient

client = MongoClient()
db = client['logins']

def addUser(username,password):
    db.users.insert({'username': username, 'passowrd': password})

def exists(username):
    user = db.users.find({'username': username}, fields = {'_id': False})
    return len([user for user in users]) != 0

def auth(username,password):
    user = db.users.find({'username': username, 'password': password}, fields = {'_id': False})
    return len([user for user in users]) != 0

def change(username, npassword):
    db.users.update({'username': username}, {'%set': {'password': npassword}})
