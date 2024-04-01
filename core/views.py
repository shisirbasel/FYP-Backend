from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import UserSerializer,ProfilePictureSerializer,LoginSerializer,BookSerializer, \
    ProfileSerializer,UpdatePasswordSerializer, VerifyAccountSerializer , ShowBookSerializer, LikeBookSerializer, GetGenresSerializer, \
    SendTradeRequestSerializer,GetTradeRequestSerializer
from core.models import User, Book, Like, Genre, TradeRequest
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.emails import send_otp
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from django.db.models import Count
from django.utils import timezone
import calendar

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
        users = User.objects.exclude(email__endswith = "@admin.com")
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=200)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user = get_object_or_404(User, id = id)
        serializer = ProfileSerializer(user, many = False)
        return Response(serializer.data, status = 200)

class UpdateProfilePictureView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
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
                return Response({"message": "Invalid Email or Password"}, status=401)
            
            if not user.is_verified:
                send_otp(user.email)
                return Response({"message": "Account Not Verified, Please Verify Your Account", "is_verified": False}, status=403)

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
            }
            return Response(data, status=201)
       
        return Response(serializer.errors, status = 400)

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
                return Response("Invalid Email", status=400)

            if user[0].otp != otp:
                return Response("Invalid OTP", status=400)
            
            user = user.first()
            user.is_verified = True
            user.save()
            return Response("Account Verified Successfully.",status=200)

        return Response("Please Try Again Later", status=400)


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
        data = Book.objects.exclude(is_traded = True)
        data = data.filter(pk__in = liked_books)
        serializer = ShowBookSerializer(instance=data, many = True)
        return Response(serializer.data)

class SendTradeRequestView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendTradeRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if 'reciprocal_trade_accepted' in serializer.validated_data:
                return Response({'message': 'Trade request accepted successfully.'}, status=200)
            else:
                serializer.save(user=request.user)
                return Response({'message': 'Trade request created successfully.'}, status=200)
        return Response(serializer.errors, status=400)

class CheckTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        requested_book = get_object_or_404(Book, pk=id)
        trade_request = TradeRequest.objects.exclude(status  = TradeRequest.RequestStatus.REJECTED)
        trade_request = trade_request.filter(user=user, requested_book=requested_book).exists()
        
        data = {
            'trade_request': trade_request,
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
        trade_request = TradeRequest.objects.exclude(status  = TradeRequest.RequestStatus.REJECTED)
        trade_request = trade_request.filter(user=user, requested_book = id).first()
        trade_request.delete()
        return Response("Trade Request Unsent", status=200)

class GetAllGenresView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Genre.objects.all()
        serializer = GetGenresSerializer(data, many=True)
        return Response(serializer.data)

class BookSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        selected_genres = request.query_params.getlist('genres', [])
        user = request.user
        
        # Initial queryset that includes all books
        queryset = Book.objects.exclude(user=user)
        queryset = queryset.exclude(is_traded = True)
        
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
        
        # Shuffle the queryset
        queryset = list(queryset)
        
        serializer = ShowBookSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
class GetUserBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        books = Book.objects.filter(user = user)
        serializer = ShowBookSerializer(books, many = True)
        return Response(serializer.data, status = 200)
    
class GetReceivedTradeRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        requests = TradeRequest.objects.filter(requested_book__user=user, status=TradeRequest.RequestStatus.PENDING).order_by("-request_date")
        serializer = GetTradeRequestSerializer(requests, many=True)
        return Response(serializer.data, status=200)

class GetSentTradeRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        requests = TradeRequest.objects.filter(user = user).order_by("-request_date")
        serializer = GetTradeRequestSerializer(requests, many = True)
        return Response(serializer.data, status = 200)
    

class RejectTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        trade_request = get_object_or_404(TradeRequest,id=id)
        trade_request.status = TradeRequest.RequestStatus.REJECTED
        trade_request.save()
        return Response("Trade Request Rejected", status=200)

class AcceptTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):

        trade_request = get_object_or_404(TradeRequest,id=id)
        trade_request.status = TradeRequest.RequestStatus.ACCEPTED
        requested_book = trade_request.requested_book
        offered_book = trade_request.offered_book
        requested_book.is_traded = True
        offered_book.is_traded = True
        requested_book.save()
        offered_book.save()
        trade_request.save()
        other_requests = TradeRequest.objects.exclude(id = id)
        other_requests = other_requests.filter(Q(requested_book = requested_book) | Q(offered_book = offered_book) | Q(offered_book = requested_book) | Q(requested_book = offered_book))
        
        for request in other_requests:
            request.status = TradeRequest.RequestStatus.INVALID
            request.save()

        return Response("Trade Request Accepted", status=200)

class CountUnseenRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        count = TradeRequest.objects.filter(status = TradeRequest.RequestStatus.PENDING, 
                        requested_book__user = user, seen = False).count()
        
        return Response({"count":count}, status= 200)

class SeeRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        requests = TradeRequest.objects.filter(status = TradeRequest.RequestStatus.PENDING, 
                        requested_book__user = user, seen = False)
        
        for request in requests:
            request.seen = True
            request.save()
        
        return Response("Trade Requests Seen", status=200)

class TopTradeMonthsView(APIView):
    def get(self, request):
        # Get the current year
        current_year = timezone.now().year

        # Calculate the trade requests count for each month of the current year
        trade_requests_by_month = TradeRequest.objects.filter(request_date__year=current_year).values('request_date__month').annotate(request_count=Count('id'))

        # Organize the data into a dictionary with month names as keys and trade request counts as values
        top_months_data = {}
        for entry in trade_requests_by_month:
            month_number = entry['request_date__month']
            month_name = calendar.month_name[month_number]  # Get month name from month number
            top_months_data[month_name] = entry['request_count']

        return Response(top_months_data, status=200)


class BookDistributionView(APIView):
    def get(self, request):
        genres = Genre.objects.all()

        distribution = {}

        for genre in genres:
            book_count = Book.objects.filter(genre=genre).count()
            distribution[genre.name] = book_count

        return Response(distribution, status=200)

class CountDetailsView(APIView):
    def get(self, request):
        books = Book.objects.all().count()
        users = User.objects.all().count() - 1
        traderequests = TradeRequest.objects.all().count()

        return Response({
            'books': books, 'users': users, 'traderequests': traderequests
        }, status=200)
    

class DeleteUserView(APIView):
    def get(self,request,username):
        user = get_object_or_404(User,username= username)
        user.delete()
        return Response("User Deleted Successfully.", status=200)
    
class ConnectedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', None)
        connected_user_ids = set()
        
        # Get the IDs of users who have sent or received trade requests with the logged-in user
        user_ids_with_requests = TradeRequest.objects.filter(user=request.user).values_list('requested_book__user_id', flat=True).distinct()
        requested_user_ids = TradeRequest.objects.filter(requested_book__user=request.user).values_list('user_id', flat=True).distinct()
        
        # Combine the IDs from both lists to get all users involved in trade requests
        connected_user_ids.update(user_ids_with_requests)
        connected_user_ids.update(requested_user_ids)

        # Exclude the logged-in user from the connected users list
        connected_user_ids.discard(request.user.id)

        if search_query:
            connected_users = User.objects.filter(id__in=connected_user_ids).filter(
                Q(username__icontains=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        else:
            connected_users = User.objects.filter(id__in=connected_user_ids)

        serializer = ProfileSerializer(connected_users, many=True)
        return Response(serializer.data, status = 200)
        
