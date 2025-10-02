from rest_framework.serializers import ModelSerializer
from .models import Users,Pledges,Fixtures,Posts,FileMetadata
import json
from bson import ObjectId
from datetime import datetime, date
from decimal import Decimal

class UserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = "__all__"

class MongoDBJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)
    
    
    
    
    
def serialize_image_document(grid_file):
    """Serialize GridFS file to JSON-serializable format specifically for images"""
    return {
        'id': str(grid_file._id),
        'filename': grid_file.filename,
        'size': grid_file.length,
        'upload_date': grid_file.upload_date.isoformat() if grid_file.upload_date else None,
        'content_type': getattr(grid_file, 'content_type', 'image/jpeg'),
        'description': getattr(grid_file, 'description', ''),
        'tags': getattr(grid_file, 'tags', []),
        'metadata': {
            'width': getattr(grid_file, 'width', None),
            'height': getattr(grid_file, 'height', None),
            'color_space': getattr(grid_file, 'color_space', None),
        }
    }    

      
class FixturesSerializer(ModelSerializer):

    class Meta:
        model=Fixtures
        fields="__all__"
    

              
class PledgesSerializer(ModelSerializer):

    class Meta:
        model=Pledges
        fields="__all__"
    
class PostsSerializer(ModelSerializer):

    class Meta:
        model=Posts
        fields="__all__"
    
class FileMetadataSerializer(ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = '__all__'    
    
