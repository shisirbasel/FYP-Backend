from rest_framework.decorators import APIView
from rest_framework.response import Response
from core.serializers import SetTradeMeetSerializer, UserSerializer,ProfilePictureSerializer,LoginSerializer,BookSerializer, \
    ProfileSerializer,UpdatePasswordSerializer, VerifyAccountSerializer , ShowBookSerializer, LikeBookSerializer, GetGenresSerializer, \
    SendTradeRequestSerializer,GetTradeRequestSerializer, NotificationSerializer, ViewProfileSerializer, ReportSerializer, \
    ViewTradeMeetSerializer, RateUserSerializer, CheckUserRatingSerializer, ViewReportSerializer, SendPasswordResetEmailSerializer, ResetPasswordSerializer
from core.models import User, Book, Like, Genre, TradeRequest, Notification, Report, TradeMeet, Rating
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.emails import send_otp
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q, Count, Avg, Max
from django.utils import timezone
import calendar
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination

class RegisterUserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        print(request.data)
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
    def get(self,request,username):
        user = get_object_or_404(User, username = username)
        if user.is_superuser:
            return Response("Cannot View Admin's profile", status=403)
        
        currentuser = request.user

        context ={
            "currentuser": currentuser,
            "user":user
        }

        serializer = ViewProfileSerializer(user, many = False, context=context)
        print(serializer.data)
        return Response(serializer.data, status = 200)
    
class UserWithIDView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user = get_object_or_404(User, id = id)
        if user.is_superuser:
            return Response("Cannot View Admin's profile", status=403)
        
        currentuser = request.user

        context ={
            "currentuser": currentuser,
            "user":user
        }

        serializer = ViewProfileSerializer(user, many = False, context=context)
        print(serializer.data)
        return Response(serializer.data, status = 200)

class CountUserBooks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        books = Book.objects.filter(user = user).count()
        return Response({'books': books}, status=200)

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
            
            if user.is_banned:
                return Response({'message': f"Your Account was Banned for multiple rules violation.", "is_verified": True, "is_banned" : user.is_banned }, status=403)
            
            if user.is_suspended:
                if datetime.now().date() >= user.suspended_date:
                    user.is_suspended = False
                    user.save()
                else:
                    return Response({'message': f"You are Suspended Until {user.suspended_date}", "is_verified": True, "is_suspended" : user.is_suspended }, status=403)
            

            login(request, user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': "Logged In Successfully",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_superuser,
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
    parser_classes =[MultiPartParser]
    def patch(self,request,id):
        book = get_object_or_404(Book, id = id)
        serializer = BookSerializer(instance=book, data = request.data, partial=True)
        print(request.data)
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
            print(request.data)
            serializer.save()
            return Response(serializer.data,status=200)
        print(request.data)
        return Response(serializer.errors, status=400)
    
class ShowProfilePictureView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        serializer = ProfilePictureSerializer(instance=user, many=False)
        return Response(serializer.data)


class UpdatePasswordView(APIView):
    parser_classes = [MultiPartParser]
    def patch(self, request):
        user = self.request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.validated_data.get('old_password')):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response("Password Changed Successfully", status=200)
            return Response("Invalid Password, Please Try again", status=400)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self,request):
        serializer = VerifyAccountSerializer(data=request.data)
        print(request.data)

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
        books = Book.objects.filter(user = user, is_traded = False)
        serializer = ShowBookSerializer(books, many = True)
        return Response(serializer.data, status = 200)
    
class GetOtherUserBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username = username)
        books = Book.objects.filter(user = user, is_traded = False)
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

class GetAcceptedTradeReqeustsView(APIView):
    
    def get(self, request):
        user = request.user
        requests = TradeRequest.objects.filter(Q(requested_book__user = user) | Q(user = user), status = TradeRequest.RequestStatus.ACCEPTED).order_by("-request_date")
        serializer = GetTradeRequestSerializer(requests, many = True)
        return Response(serializer.data, status = 200)

class GetRejectedTradeRequestsView(APIView):
    def get(self, request):
        user = request.user
        requests = TradeRequest.objects.filter(Q(requested_book__user = user) | Q(user = user), status = TradeRequest.RequestStatus.REJECTED).order_by("-request_date")
        serializer = GetTradeRequestSerializer(requests, many = True)
        return Response(serializer.data, status = 200)
    

class RejectTradeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        trade_request = get_object_or_404(TradeRequest,id=id)
        trade_request.status = TradeRequest.RequestStatus.REJECTED
        trade_request.save()

        Notification.objects.create(user = trade_request.user,
                                     message = f"Your traderequest for {trade_request.requested_book} was rejected.")
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

        Notification.objects.create(user = trade_request.user, message = f"Your Traderequest for {requested_book.title} was accepted.")
        
        
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

        top_months_data = {}
        for entry in trade_requests_by_month:
            month_number = entry['request_date__month']
            month_name = calendar.month_name[month_number] 
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
        users = User.objects.exclude(email__endswith = '@admin.com').count()
        traderequests = TradeRequest.objects.all().count()

        return Response({
            'books': books, 'users': users, 'traderequests': traderequests
        }, status=200)
    

class DeleteUserView(APIView):
    def delete(self,request,username):
        user = get_object_or_404(User,username= username)
        user.delete()
        return Response("User Deleted Successfully.", status=200)
    
class ConnectedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', None)
        connected_user_ids = set()
        
        user_ids_with_requests = TradeRequest.objects.filter(user=request.user).values_list('requested_book__user_id', flat=True).distinct()
        requested_user_ids = TradeRequest.objects.filter(requested_book__user=request.user).values_list('user_id', flat=True).distinct()
        
        connected_user_ids.update(user_ids_with_requests)
        connected_user_ids.update(requested_user_ids)

        connected_user_ids.discard(request.user.id)

        if search_query:
            connected_users = User.objects.filter(id__in=connected_user_ids).filter(
                Q(username__icontains=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        else:
            current_user = request.user
            connected_users = User.objects.filter(
                Q(sender__receiver=current_user) | Q(receiver__sender=current_user)
            ).distinct()

        serializer = ProfileSerializer(connected_users, many=True)
        return Response(serializer.data, status = 200)
    
class GetNotificationsView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
        serializer = NotificationSerializer(notifications, many = True)
        return Response(serializer.data, status = 200)

class CountUnseenNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        count = Notification.objects.filter(user = request.user, seen = False).count()
        return Response({'count': count}, status= 200)

class SeeNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        notifications = Notification.objects.filter(user = request.user, seen = False)
        for notification in notifications:
            notification.seen = True
            notification.save()
        return Response("Notifications Seen.", status=200)


class RecommendBooksView(APIView):
    def get(self, request):
        user = request.user
        chosen_genres = user.genre.all()
        top_traded_genres = TradeRequest.objects.filter(user=user).values('requested_book__genre').annotate(total_trades=Count('id')).order_by('-total_trades')[:4]
        
        recommended_genres = set(chosen_genres) | set(Genre.objects.filter(id__in=top_traded_genres.values_list('requested_book__genre', flat=True)))

        recommended_books = Book.objects.filter(genre__in=recommended_genres).exclude(user=user).exclude(is_traded = True).distinct()[:10]  # Limit =
        serializer = ShowBookSerializer(recommended_books, many=True)
        return Response(serializer.data, status=200)

class ReportTypeView(APIView):
    def get(self, request):
        report_types = dict(Report.ReportType.choices)
        return Response({'report_types': report_types}, status=200)

class ReportUserView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        reported_user_id = id
        reported_by_user = request.user
        report_type = request.data.get('type')
        description = request.data.get('description')


        report_data = {
            'reported_by': reported_by_user.id,
            'reported_user': reported_user_id,
            'type': report_type,
            'description': description
        }
        serializer = ReportSerializer(data=report_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class GetDistrictsView(APIView):
   def get(self, request):
        districts = [choice[0] for choice in TradeMeet.DISTRICT_CHOICES]
        return Response({'districts': districts})

class SetTradeMeetView(APIView):
    parser_classes=[MultiPartParser]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        sender = request.user
        traderequest = TradeRequest.objects.get(id = request.data.get('traderequest'))

        receiver = traderequest.requested_book.user
        if receiver == sender:
            receiver = traderequest.offered_book.user
        
        data = request.data.copy()
        data['sender'] = sender.id
        data['receiver'] = receiver.id
        
        serializer = SetTradeMeetSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            Notification.objects.create(user = receiver, message =f"{sender.username} has set a new Trademeet.")
            return Response({'success': 'Trade meet set successfully'}, status=201)
        
        return Response(serializer.errors, status=400)

class GetTradeMeetView(APIView):
    def get(self, request, id):
        trademeet = TradeMeet.objects.filter(traderequest__id = id).order_by('-date').first()
        serializer = ViewTradeMeetSerializer(trademeet, many = False)
        return Response(serializer.data, status=200)

class RateUserView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = {
            'rater': request.user.id,
            'user': User.objects.get(id=id).id,
            'rating': request.data.get('rating')
        }
        
        serializer = RateUserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response("User Rated Successfully.", status=201)
        return Response(serializer.errors, status=400)

class UpdateUserRatingView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def patch(self, request, username):
        rater = request.user
        user = get_object_or_404(User, username=username)
        
        try:
            rating = Rating.objects.get(rater=rater, user=user)
        except Rating.DoesNotExist:
            rating = Rating(rater=rater, user=user)

        serializer = RateUserSerializer(instance=rating, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response("User Rated Successfully.", status=200)
        return Response(serializer.errors, status=400)

class CheckUserRatingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        rater = request.user
        user = User.objects.get(username=username)
        
        try:
            rating = Rating.objects.get(rater=rater, user=user)
            serializer = CheckUserRatingSerializer(rating)
            return Response(serializer.data, status=200)
        except Rating.DoesNotExist:
            return Response("Rating does not exist.", status=404)

class GetAvgUserRatingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user_ratings = Rating.objects.filter(user__username=username)
        avg_rating = user_ratings.aggregate(Avg('rating'))['rating__avg']
        return Response({"rating": avg_rating}, status=200)

class SuspendUserView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        user = User.objects.get(id=id)
        user.suspend_count += 1

        if user.suspend_count >=3:
            user.is_banned = True
        
        user.suspended_date = datetime.now() + timedelta(days=7)
        user.is_suspended = True
        user.save()
        return Response("User Suspended Successfully", status=200)

class ViewAllReports(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reports = Report.objects.all().order_by('-report_date')
        serializer = ViewReportSerializer(reports, many = True)
        return Response(serializer.data,status=200)

class CheckUserStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        status = User.objects.get(id = id).is_suspended
        return Response({'status': status}, status = 200)


class GetAllTradeRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination 
    
    def get(self, request):
        paginator = self.pagination_class()
        requests = TradeRequest.objects.all().order_by('-request_date')
 
        page = paginator.paginate_queryset(requests, request)

        if page is not None:
            serializer = GetTradeRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = GetTradeRequestSerializer(requests, many=True)
        return Response(serializer.data, status=200)

class GetAllTradeMeetsView(APIView):
    def get(self, request):
        # Annotate the TradeMeet queryset to get the maximum created_date for each traderequest
        latest_dates = TradeMeet.objects.values('traderequest_id').annotate(max_date=Max('created_date'))
        
        # Get the distinct TradeRequest objects with the most recent created_date
        distinct_traderequests = TradeMeet.objects.filter(
            id__in=[item['traderequest_id'] for item in latest_dates]
        ).order_by('traderequest_id', '-created_date').distinct('traderequest_id')
        

        serializer = ViewTradeMeetSerializer(distinct_traderequests, many=True)
        
        return Response(serializer.data, status=200)
    
class GetTodayTradeMeetView(APIView):
    def get(self, request):
        today_date = datetime.now().date()
        
        # Annotate the TradeMeet queryset to get the maximum date for each traderequest
        latest_dates = TradeMeet.objects.filter(date=today_date).values('traderequest_id').annotate(max_date=Max('date'))
        
        # Get the distinct TradeMeet objects with the most recent date
        distinct_trademeets = TradeMeet.objects.filter(
            traderequest_id__in=[item['traderequest_id'] for item in latest_dates],
            date__in=[item['max_date'] for item in latest_dates]
        ).order_by('-date')
        
        serializer = ViewTradeMeetSerializer(distinct_trademeets, many=True)
        return Response(serializer.data, status=200)
    
class CheckAcceptedReqeustView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user =  User.objects.get(username = username)
        if TradeRequest.objects.filter(Q(requested_book__user = request.user, offered_book__user = user) | Q(requested_book__user = user, offered_book__user = request.user), status = TradeRequest.RequestStatus.ACCEPTED).exists():
            return Response({'exists':True}, status = 200)
        return Response({'exists': False}, status=200)

    
class GetTomorrowTradeMeetView(APIView):
    def get(self, request):
        tomorrow_date = datetime.now().date() + timedelta(days=1)
        
        # Annotate the TradeMeet queryset to get the maximum date for each traderequest
        latest_dates = TradeMeet.objects.filter(date=tomorrow_date).values('traderequest_id').annotate(max_date=Max('date'))
        
        # Get the distinct TradeMeet objects with the most recent date
        distinct_trademeets = TradeMeet.objects.filter(
            traderequest_id__in=[item['traderequest_id'] for item in latest_dates],
            date__in=[item['max_date'] for item in latest_dates]
        ).order_by('-date')
        
        serializer = ViewTradeMeetSerializer(distinct_trademeets, many=True)
        return Response(serializer.data, status=200)

class GetWeekTradeMeetView(APIView):
    def get(self, request):
        tomorrow_date = datetime.now().date() + timedelta(days=1)
        end_of_week = datetime.now().date() + timedelta(days=7)
        
        # Annotate the TradeMeet queryset to get the maximum date for each traderequest
        latest_dates = TradeMeet.objects.filter(date__gt=tomorrow_date, date__lte=end_of_week).values('traderequest_id').annotate(max_date=Max('date'))
        
        # Get the distinct TradeMeet objects with the most recent date
        distinct_trademeets = TradeMeet.objects.filter(
            traderequest_id__in=[item['traderequest_id'] for item in latest_dates],
            date__in=[item['max_date'] for item in latest_dates]
        ).order_by('-date')
        
        serializer = ViewTradeMeetSerializer(distinct_trademeets, many=True)
        return Response(serializer.data, status=200)
    
class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid():
            return Response("Password Reset Link Sent.", status= 201)
        print(serializer.errors)
        return Response(serializer.errors, status= 400)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data = request.data, context ={"uid": uid, "token":token})
        if serializer.is_valid():
            return Response("Password Reset Successfully.", status=200)
        return Response(serializer.errors, status=400)