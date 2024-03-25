from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import UserSerializer,ProfilePictureSerializer,LoginSerializer,BookSerializer, \
    ProfileSerializer,UpdatePasswordSerializer, VerifyAccountSerializer , ShowBookSerializer, LikeBookSerializer, GetGenresSerializer, \
    TradeRequestSerializer
from core.models import User, Book, Like, Genre, TradeRequest
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.emails import send_otp
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q


class RegisterUserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            send_otp(serializer.data['email'])
            data = {
                'message': 'User Registered Successfully',
                'data': serializer.data
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)

class ShowUsersView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)

class UpdateProfilePictureView(APIView):
    def patch(self,request,id):
        user = request.user 
        serializer = ProfilePictureSerializer(instance=user, data = request.data)
        if serializer.is_valid():
            serializer.save(user,request.data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            
            if user is None:
                return Response("Invalid email or password", status=401)

            login(request, user)
            
            refresh = RefreshToken.for_user(user)
            
           
            
            return Response({
                'message': "Logged In Successfully",
                'refresh': {
                    'token': str(refresh),
                },
                'access': {
                    'token': str(refresh.access_token),
                },
                'user': {
                    'is_admin': user.is_superuser
                }
            }, status=200)
        
        return Response(serializer.errors, status=400)
    
        
class AddBookView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self,request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            data = {
                'message': 'Book Added Successfully',
                'data': serializer.data,
                'status':201
            }
            return Response(data)
        data = {
            "message":"Invalid Input",
            "status":400,
            "errors":serializer.errors
        }
        return Response(data)

class UpdateBookView(APIView):
    def patch(self,request,id):
        book = get_object_or_404(Book, id = id)
        serializer = BookSerializer(instance=book, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors, status=400)
    
class ShowBooksView(APIView):
    def get(self,request):
        data = Book.objects.all()
        serializer = ShowBookSerializer(data, many = True)
        return Response(serializer.data)
    
class DeleteBookView(APIView):
    def delete(self,request,id):
        book = get_object_or_404(Book,id=id)
        book.delete()
        return Response("Book has been Deleted..", status=200)
    
class ShowProfileView(APIView):
    def get(self,request):
        user = request.user
        serializer = ProfileSerializer(user,many = False)
        return Response(serializer.data)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def patch(self,request):
        user = self.request.user
        serializer = ProfileSerializer(instance=user, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors, status=400)
    
class ShowProfilePictureView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        serializer = ProfilePictureSerializer(instance=user, many=False)
        return Response(serializer.data)


class UpdatePasswordView(APIView):
    def patch(self, request):
        user = self.request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.validated_data.get('old_password')):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response({"message": "Password Changed Successfully"}, status=200)
            return Response({"error": "Invalid Password"}, status=400)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):

    def post(self,request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)
            if not user.exists():
                return Response({'status':'400', 'message':'Invalid Email'})

            if user[0].otp != otp:
                return Response({'status':'400', 'message':'Invalid OTP'})

            user = user.first()
            user.is_verified = True
            user.save()
            return Response({'status':'200', 'message':'account verified'})

        return Response({'status':'400', 'data': serializer.errors})


class LikeBookView(APIView):

    parser_classes = [MultiPartParser]

    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LikeBookSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            book_id = serializer.validated_data.get('book_id')
            book = get_object_or_404(Book, pk=book_id)
            
            like_exists = Like.objects.filter(user=user, book=book).exists()
            if like_exists:
                Like.objects.filter(user=user, book=book).delete()
                return Response({'liked': False}, status=200)

            Like.objects.create(user=user, book=book)
            return Response({'liked': True}, status=201)
        
        return Response(serializer.errors, status=400)
    
class CheckLikedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        user = request.user
        book = get_object_or_404(Book, pk=id)
        
        like_exists = Like.objects.filter(user=user, book=book).exists()
        return Response({'liked': like_exists}, status=200)
    
class GetLikedBookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_books = Like.objects.filter(user=user).values_list('book', flat=True)
        data = Book.objects.filter(pk__in = liked_books)
        serializer = ShowBookSerializer(instance=data, many = True)
        return Response(serializer.data)

class SendTradeRequestView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TradeRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Trade request created successfully.'}, status=201)
        
        return Response(serializer.errors, status=400)

class GetTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        requested_book = get_object_or_404(Book, pk=id)
        trade_request = TradeRequest.objects.filter(user=user, requested_book=requested_book).exists()
        
        data = {
            'trade_request': trade_request ,
            'user_id': user.id,
            'requested_book': {
                'id': requested_book.id,
                'title': requested_book.title,
            }
        }
        
        
        return Response(data, status=200)

class DeleteTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = request.user
        trade_request = TradeRequest.objects.filter(user=user, requested_book = id).first()
        trade_request.delete()
        return Response("Trade Request Unsent", status=200)

class GetAllGenresView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Genre.objects.all()
        serializer = GetGenresSerializer(data, many=True)
        return Response(serializer.data)

class BookSearchAPIView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')
        selected_genres = request.query_params.getlist('genres', [])
        user = request.user
        
        # Initial queryset that includes all books
        queryset = Book.objects.exclude(user = user)
        
        # Filter by search query if provided
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            )
        
        # Apply genre filters if selected genres are provided
        if selected_genres:
            genre_filters = [Q(genre__name__icontains=genre) for genre in selected_genres]
            combined_filter = Q()
            for q in genre_filters:
                combined_filter |= q
            queryset = queryset.filter(combined_filter)
        
        
        serializer = ShowBookSerializer(queryset, many=True)
        return Response(serializer.data, status=200)


class GetUserBooksView(APIView):
    def get(self, request):
        user = request.user
        books = Book.objects.filter(user = user)
        serializer = ShowBookSerializer(books, many = True)
        return Response(serializer.data, status = 200)
        