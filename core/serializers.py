from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Book

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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False) 
    
    class Meta:
        model = get_user_model()
        fields = ["profile_picture"]
    
    def save(self,user,data):
        user.profile_picture = data.get("profile_picture")
        user.save()
        return user

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [ 'title',
                    'author',
                    'is_traded',
                    'genre',
                    'upload_date',
                    'user',
                    'image',
                    ]
        
        read_only_fields = ['user']

    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =get_user_model()
        fields = "__all__"

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


