from django.urls import path
from core.views import (
    RegisterUserView,ShowUsersView,UpdateProfilePictureView, LoginUserView, AddBookView, 
    UpdateBookView,ShowBooksView,DeleteBookView,ShowProfileView,UpdateProfileView,UpdatePasswordView,VerifyOTPView,
    LikeBookView, GetAllGenresView,GetUserBooksView, BookSearchAPIView, SendTradeRequestView, CheckTradeRequestView, DeleteTradeRequestView,
    CheckLikedView, GetLikedBookView,GetReceivedTradeRequestsView, AcceptTradeRequestView, RejectTradeRequestView, GetSentTradeRequestsView,
    CountUnseenRequestView, SeeRequestsView, TopTradeMonthsView, BookDistributionView, CountDetailsView, DeleteUserView
            )

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),
    path('login/',LoginUserView.as_view(),name="login"),
    path('profile_picture/',UpdateProfilePictureView.as_view(),name="profile_picture"),
    path('update_profile/',UpdateProfileView.as_view(),name="update_profile"),
    path('update_password/',UpdatePasswordView.as_view(),name="update_password"),
    path('update_password/',UpdatePasswordView.as_view(),name="update_password"),
    path('profile/',ShowProfileView.as_view(),name="show_profile"),
    path('add_book/',AddBookView.as_view(),name="add_book"),
    path('update_book/<int:id>/',UpdateBookView.as_view(),name="update_book"),
    path('show_books/',ShowBooksView.as_view(),name="show_books"),
    path('delete_book/<int:id>/',DeleteBookView.as_view(),name="delete_book"),
    path('verify_account/',VerifyOTPView.as_view(),name="verify_otp"),
    path('like/',LikeBookView.as_view(), name='like_book'),
    path('liked_books/',GetLikedBookView.as_view(), name='liked_books'),
    path('check_like/<int:id>/',CheckLikedView.as_view(), name='check_like'),
    path('genres/',GetAllGenresView.as_view(), name="genres"),
    path('yourbooks/',GetUserBooksView.as_view(), name="yourbooks"),
    path('books/search/', BookSearchAPIView.as_view(), name='book_search'),
    path('send/traderequest/',SendTradeRequestView.as_view(), name="send_trade_request"),
    path('get/traderequest/<int:id>/',CheckTradeRequestView.as_view(), name="check_trade_request"),
    path('delete/traderequest/<int:id>/',DeleteTradeRequestView.as_view(), name="delete_trade_request"),
    path('get/received_traderequests/',GetReceivedTradeRequestsView.as_view(), name="get_received_requests"),
    path('get/sent_traderequests/',GetSentTradeRequestsView.as_view(), name="get_sent_requests"),
    path('reject/traderequest/<int:id>/',RejectTradeRequestView.as_view(), name="reject_received_request"),
    path('accept/traderequest/<int:id>/',AcceptTradeRequestView.as_view(), name="accept_received_request"),
    path('count_unseen_requests/',CountUnseenRequestView.as_view(), name="request_count" ),
    path('see_requests/',SeeRequestsView.as_view(), name="see_requests" ),
    path('top_month/', TopTradeMonthsView.as_view(), name="top_month"),
    path("books_distribution/", BookDistributionView.as_view(), name="book_distribution"),
    path("countdetails/", CountDetailsView.as_view(), name="count_details"),
    path("delete_user/<str:username>", DeleteUserView.as_view(), name="delete_user"),

    #jwt token 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]