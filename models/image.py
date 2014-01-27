# Models and Collections for images
from datetime import datetime
from models.base import Collection, Model
from models.review import Comment
from models.tag import Tag


''' Format for an insert would be:
    image.insert(user=...,image=...)
'''
class ImageModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(CartModel, self).__init__(db, fs, collection, obj)

    # Adds tag to image
    def add_tag(self, label):
        tags = Tag()
        t = tags.find_one(label=label)
        if not t:
            t = tags.insert(label=label)
        if not any(d['label'] == label for d in self.tags):
            t.count += 1
            t.save()
            t._obj.pop('count')
            self.tags.append(t._obj)
            self.save()
            return True
        return False

    # Adds a comment under the users page
    def add_comment(self, user, **kwargs):
        comments = Comment()
        c = comments.insert(img_id=self.get_id(), user=user, **kwargs)
        self.save()
        return c

    # Get blog reviews made by this user, and with other arguments
    def get_comments(self, **kwargs):
        comments = Comment()
        return comments.find(img_id=self.get_id(), **kwargs)


class Image(Collection):

    def __init__(self):
        super(Image, self).__init__(ImageModel)

    def insert(self, **kwargs):
        return super(Image, self).insert(tags=[], **kwargs)

    # Get by tag function
    def get_by_tag(self, label):
        return self.to_objects(self.objects.find({'tags': {'$elemMatch':
            {'label': label}}}).sort([('date', -1)]))
