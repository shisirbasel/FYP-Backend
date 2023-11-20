from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ""),
            last_name=validated_data.get('last_name', ""),
        )
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name',]  
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False) 
    
    class Meta:
        model = get_user_model()
        fields = ["profile_picture"]
    
    def save(self,user,data):
        user.profile_picture = data.get("profile_picture")
        user.save()
        return user