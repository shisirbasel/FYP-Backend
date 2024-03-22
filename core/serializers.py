from rest_framework import serializers
from core.models import Book, Genre, User, TradeRequest


class GetGenresSerializer(serializers.ModelSerializer):
     class Meta:
         model = Genre
         fields = ['id','name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ""),
            last_name=validated_data.get('last_name', ""),
            username=validated_data.get('username', ""),
        )

        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name','username']  
        extra_kwargs = {
            'password': {'write_only': True}
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False) 
    
    class Meta:
        model = User
        fields = ["profile_picture"]
    
    def save(self,user,data):
        user.profile_picture = data.get("profile_picture")
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:

        model = Book
        fields = ['title', 'author', 'genre', 'upload_date', 'user', 'image']
        read_only_fields = ['user']

class ShowBookSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'is_traded', 'genre', 'upload_date', 'user', 'image']

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','profile_picture','genre']
        read_only_fields = ['profile_picture']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LikeBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Invalid book ID")

        return value

class TradeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRequest
        fields = ['user', 'requested_book', 'offered_book']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        requested_book = data['requested_book']
        
        existing_trade_request = TradeRequest.objects.filter(user=user, requested_book=requested_book).exists()

        if existing_trade_request:
            raise serializers.ValidationError("You have already sent a trade request for this book combination.")
        
        return data
    

