from djoser.serializers import UserCreateSerializer as BaseUserCreateSerailizer 

# Import Custom User
from django.contrib.auth import get_user_model
User = get_user_model()



class UserCreateSerializer(BaseUserCreateSerailizer):
    
    
    class Meta(BaseUserCreateSerailizer.Meta):
        model = User
        fields = ['id', 'email', 'password', 'account_type']


    