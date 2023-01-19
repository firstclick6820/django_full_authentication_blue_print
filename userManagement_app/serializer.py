# import Rest framework
from rest_framework import serializers



# import custom models
from .models import User, Profile




class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields ="__all__"



