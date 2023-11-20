from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import UserSerializer,ProfilePictureSerializer
from core.models import User, Book

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