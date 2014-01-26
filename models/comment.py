# Models and Collections for comments
from models.base import Collection, Model


''' Format for an insert would be:
    comment.insert(text=...,img_id=...)
'''
class CommentModel(Model):

    def __init__(self, db, fs, collection, obj):
        super(CommentModel, self).__init__(db, fs, collection, obj)


class Comment(Collection):

    def __init__(self):
        super(Comment, self).__init__(ReviewModel)

    def insert(self, **kwargs):
        return super(Comment, self).insert(**kwargs)
