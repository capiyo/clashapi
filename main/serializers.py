from rest_framework.serializers import ModelSerializer
from .models import Users,Pledges,Fixtures

class UserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = "__all__"



      
class FixturesSerializer(ModelSerializer):

    class Meta:
        model=Fixtures
        fields="__all__"
    

              
class PledgesSerializer(ModelSerializer):

    class Meta:
        model=Pledges
        fields="__all__"
    
