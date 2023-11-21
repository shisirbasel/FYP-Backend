from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import UserSerializer,ProfilePictureSerializer,LoginSerializer,BookSerializer
from core.models import User, Book
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class RegisterUserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ShowUsersView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)

class UploadProfilePictureView(APIView):
    def patch(self,request,id):
        user = request.user 
        serializer = ProfilePictureSerializer(instance=user, data = request.data)
        if serializer.is_valid():
            serializer.save(user,request.data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class LoginUserView(APIView):
    def post(self,request):
        try:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email = email, password = password)
                
                if user is None:
                    return Response(serializer.errors, status=400)
                
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            
            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response(f"Error Occurred, Exception:{e}")
        
class AddBookView(APIView):
    def post(self,request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)

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
        serializer = BookSerializer(data, many = True)
        return Response(serializer.data) 