from pymongo import MongoClient
from django.conf import settings
import gridfs

class MongoDBManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
            cls._initialize_connection()
        return cls._instance
    
    @classmethod
    def _initialize_connection(cls):
        try:
            cls.client = MongoClient(
                settings.DATABASES['default']['CLIENT']['host'],
                maxPoolSize=50,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000
            )
            db_name = settings.DATABASES['default']['NAME']
            cls.db = cls.client[db_name]
            cls.fs = gridfs.GridFS(cls.db)
            
            # Create indexes for better performance
            cls.db.fs.files.create_index('uploadDate')
            cls.db.fs.files.create_index('filename')
            cls.db.fs.files.create_index('content_type')
            cls.db.fs.files.create_index('tags')
            
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            raise
    
    @classmethod
    def get_gridfs(cls):
        return cls.fs
    
    @classmethod
    def get_database(cls):
        return cls.db
    
    @classmethod
    def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls._instance = None

mongodb_manager = MongoDBManager()