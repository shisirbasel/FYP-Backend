from rest_framework import serializers
from core.models import Book, Genre, User, TradeRequest, Notification, Report, TradeMeet, Rating
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from core.emails import send_password_reset_email
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
    
    def validate(self, obj):
        genre = obj.get('genre')
        if not genre:
            raise serializers.ValidationError("Genre must be provided.")
        return obj

class ShowBookSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    genre = GetGenresSerializer()
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'is_traded', 'genre', 'user', 'image']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','username','email','profile_picture','genre']
        read_only_fields = ['profile_picture']
    
class ViewProfileSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()
    genre = GetGenresSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile_picture', 'genre', 'is_me']
        read_only_fields = ['profile_picture']

    def get_is_me(self, obj):
        return self.context['currentuser'] == self.context['user']


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

class SendTradeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRequest
        fields = ['user', 'requested_book', 'offered_book']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        requested_book = data['requested_book']
        offered_book = data['offered_book']
        trade_request = TradeRequest.objects.filter(requested_book=offered_book, offered_book=requested_book).first()
        if trade_request:
            TradeRequest.objects.create(
                user = user,
                offered_book = offered_book,
                requested_book = requested_book,
                status = TradeRequest.RequestStatus.ACCEPTED
            )
            trade_request.status = TradeRequest.RequestStatus.ACCEPTED
            trade_request.save()

            requested_book = trade_request.requested_book
            requested_book.is_traded = True
            requested_book.save()

            offered_book = trade_request.offered_book
            offered_book.is_traded = True
            offered_book.save()

            Notification.objects.create(
                user = requested_book.user,
                message = f"Your Trade Request for {offered_book.title} was accepted."
            )

            Notification.objects.create(
                user = offered_book.user,
                message = f"Your Trade Request for {requested_book.title} was accepted."
            )

            data['reciprocal_trade_accepted'] = True
        
        existing_trade_request = TradeRequest.objects.filter(status = TradeRequest.RequestStatus.PENDING)
        existing_trade_request = existing_trade_request.filter(user=user, requested_book=requested_book).exists()
        
        if existing_trade_request:
            raise serializers.ValidationError("You have already sent a trade request for this book combination.")
        
        return data


class GetTradeRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    requested_book = ShowBookSerializer()
    offered_book = ShowBookSerializer()
    class Meta:
        model = TradeRequest
        fields = ['id', 'user', 'requested_book', 'offered_book', 'status']
    

class NotificationSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date.strftime('%d %b %Y, %H:%M')

    class Meta:
        model = Notification
        fields = ['message', 'date', 'seen']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['reported_by','reported_user','description','type']

class ViewReportSerializer(serializers.ModelSerializer):
    reported_by = ProfileSerializer()
    reported_user = ProfileSerializer()
    class Meta:
        model = Report
        fields = ['reported_by','reported_user','description','type']
    

class ViewTradeMeetSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    receiver = ProfileSerializer()
    traderequest = GetTradeRequestSerializer()
    class Meta:
        model = TradeMeet
        fields = ['date','time','place','district','traderequest','sender','receiver']
    
class SetTradeMeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeMeet
        fields = ['date','time','place','district','traderequest','sender','receiver']
    
class RateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['rater', 'user', 'rating']

    def create(self, validated_data):
        rating_value = validated_data.get('rating')

        if rating_value > 5:
            raise serializers.ValidationError("Maximum Rating is 5.")
        if rating_value < 0:
            raise serializers.ValidationError("Minimum Rating is 0.")

        return Rating.objects.create(**validated_data)


class CheckUserRatingSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Rating
        fields = ['rater', 'user', 'rating']


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ["email"]
    
    def validate(self, obj):
        email = obj.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = "http://localhost:3000/forgot-password/reset/" + uid+'/'+token
            send_password_reset_email(user.email, link)
            return obj
        else :
            raise serializers.ValidationError("Email not found")

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, obj):
        try:
            password = obj.get('password')
            password2 = obj.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Link is expired or invalid.')
            user.set_password(password)
            user.save()
            return obj
        except Exception:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Link is expired or invalid')