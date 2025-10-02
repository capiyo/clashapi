from pymongo import MongoClient
from django.conf import settings

def get_mongodb_connection():
    """Get MongoDB database connection"""
    client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
    db_name = settings.DATABASES['default']['NAME']
    return client[db_name]

def get_gridfs():
    """Get GridFS instance"""
    import gridfs
    db = get_mongodb_connection()
    return gridfs.GridFS(db)