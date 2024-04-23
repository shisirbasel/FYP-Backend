from django.urls import path
from core.views import (
    RegisterUserView,ShowUsersView,UpdateProfilePictureView, LoginUserView, AddBookView, 
    UpdateBookView,ShowBooksView,DeleteBookView,ShowProfileView,UpdateProfileView,UpdatePasswordView,VerifyOTPView,
    LikeBookView, GetAllGenresView,GetUserBooksView, BookSearchAPIView, SendTradeRequestView, CheckTradeRequestView, DeleteTradeRequestView,
    CheckLikedView, GetLikedBookView,GetReceivedTradeRequestsView, AcceptTradeRequestView, RejectTradeRequestView, GetSentTradeRequestsView,
    CountUnseenRequestView, SeeRequestsView, TopTradeMonthsView, BookDistributionView, CountDetailsView, DeleteUserView, ConnectedUsersView,
    UserView,GetNotificationsView, CountUnseenNotificationsView, SeeNotificationsView, GetAcceptedTradeReqeustsView, GetRejectedTradeRequestsView, RecommendBooksView, GetOtherUserBooksView, ReportTypeView, ReportUserView, GetDistrictsView, SetTradeMeetView, GetTradeMeetView, UserWithIDView,
    RateUserView, UpdateUserRatingView, CheckUserRatingView, GetAvgUserRatingView, SuspendUserView, ViewAllReports, CheckUserStatusView, GetAllTradeMeetsView, GetTodayTradeMeetView,GetAllTradeRequestsView, GetTomorrowTradeMeetView, GetWeekTradeMeetView,CheckAcceptedReqeustView, SendPasswordResetEmailView,ResetPasswordView, GetOwnAvgUserRatingView
            )

from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),
    path('login/',LoginUserView.as_view(),name="login"),
    path('user/<int:id>/', UserWithIDView.as_view(), name="user_id"),
    path('user/<str:username>/', UserView.as_view(), name="user_username"),
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
    path('get/rejected_traderequests/',GetRejectedTradeRequestsView.as_view(), name="get_rejected_requests"),
    path('get/accepted_traderequests/',GetAcceptedTradeReqeustsView.as_view(), name="get_accepted_requests"),
    path('reject/traderequest/<int:id>/',RejectTradeRequestView.as_view(), name="reject_received_request"),
    path('accept/traderequest/<int:id>/',AcceptTradeRequestView.as_view(), name="accept_received_request"),
    path('count_unseen_requests/',CountUnseenRequestView.as_view(), name="request_count" ),
    path('see_requests/',SeeRequestsView.as_view(), name="see_requests" ),
    path('top_month/', TopTradeMonthsView.as_view(), name="top_month"),
    path("books_distribution/", BookDistributionView.as_view(), name="book_distribution"),
    path("countdetails/", CountDetailsView.as_view(), name="count_details"),
    path("delete_user/<str:username>", DeleteUserView.as_view(), name="delete_user"),
    path("get_connected_users/",ConnectedUsersView.as_view(), name="conntected_user"),
    path("notifications/",GetNotificationsView.as_view(), name="notifications"),
    path("unseen_notifications/",CountUnseenNotificationsView.as_view(), name="unseen_notifications"),
    path("see_notifications/",SeeNotificationsView.as_view(), name="see_notifications"),
    path("recommendation/",RecommendBooksView.as_view(), name="recommendatations"),
    path("books/<str:username>/",GetOtherUserBooksView.as_view(), name="other_user_books"),
    path("report_types/",ReportTypeView.as_view(), name="report_type"),
    path("report_user/<int:id>/",ReportUserView.as_view(), name="report_user"),
    path("districts/",GetDistrictsView.as_view(), name="districts"),
    path("set_trademeet/",SetTradeMeetView.as_view(), name="set_trademeet"),
    path("view_trademeet/<int:id>/",GetTradeMeetView.as_view(), name="get_trademeet"),
    path("rate_user/<int:id>/",RateUserView.as_view(), name="rate_user"),
    path("update_user_rating/<str:username>/",UpdateUserRatingView.as_view(), name="update_rate_user"),
    path("get_user_rating/<str:username>/",CheckUserRatingView.as_view(), name="get_rate_user"),
    path("avg_user_rating/<str:username>/",GetAvgUserRatingView.as_view(), name="get_rate_user"),
    path("own_rating/",GetOwnAvgUserRatingView.as_view(), name="own_rating"),
    path("reports/",ViewAllReports.as_view(), name="reports"),
    path("suspend/<int:id>/",SuspendUserView.as_view(), name="suspend_user"),
    path("status/<int:id>/",CheckUserStatusView.as_view(), name="user_status"),
    path("all_traderequests/",GetAllTradeRequestsView.as_view(), name="all_traderequests"),
    path("all_trademeets/",GetAllTradeMeetsView.as_view(), name="all_trademeets"),
    path("today_trademeets/",GetTodayTradeMeetView.as_view(), name="today_trademeet"),
    path("tomorrow_trademeets/",GetTomorrowTradeMeetView.as_view(), name="tomorrow_trademeet"),
    path("week_trademeets/",GetWeekTradeMeetView.as_view(), name="week_trademeet"),
    path("check_request/<str:username>/",CheckAcceptedReqeustView.as_view(), name="check_request"),
    path("send_reset_password_email/",SendPasswordResetEmailView.as_view(), name="reset-password-email"),
    path("reset_password/<str:uid>/<str:token>/",ResetPasswordView.as_view(), name="reset-password"),
    
    #jwt token 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),


]