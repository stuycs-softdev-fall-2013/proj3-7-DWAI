# Models and Collections for users
from models.base import Collection, Model

''' Format for an insert would be:
    users.insert(username=...,password=...,pic=...)
'''
class UserModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(UserModel, self).__init__(db, fs, collection, obj)

    # Change password with authentication
    def change_password(self, oldpass, newpass, confirm):
        if oldpass == self.password:
            if newpass == confirm:
                self.password = newpass
                self.save()
                return True
        return False

    # Change password with authentication
    def change_username(self, password, newusr):
        if password == self.password and not self.collection.exists(newusr):
            self.username = newusr
            self.save()
            return True
        return False

    # Change profile picture
    def change_propic(self, image_file):
        image_id = self.fs.put(image_file.read())
        img = {'_id': image_id}
        self.pic = img
        self.save()

class User(Collection):

    def __init__(self):
        super(User, self).__init__(UserModel)

    def insert(self, **kwargs):
        return super(User, self).insert(**kwargs)

    # Checks if a specific user exists
    def exists(self, username):
        return self.find_one(username=username) is not None

    def authenticate(self, username, password):
	return self.find_one(username=username, password=password) is not None
