# Application
SECRET_KEY = "my super secret key"

# Mongodb
DB_NAME = 'backend'
COLLECTIONS = {
        'User': 'users',
        'Tag': 'tags',
        'Collection': 'ignore'
        }

IGNORE_ATTRS = ['_obj', 'collection', 'fs', 'db']

# Elasticsearch
ES_REPEAT = 5
