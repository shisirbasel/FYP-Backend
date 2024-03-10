from django.urls import path
from core.views import (
    RegisterUserView,ShowUsersView,UpdateProfilePictureView, LoginUserView, AddBookView, 
    UpdateBookView,ShowBooksView,DeleteBookView,ShowProfileView,UpdateProfileView,UpdatePasswordView,VerifyOTPView,
    LikeBookView, GetAllGenresView,GetOwnBooksView
            )

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),
    path('login/',LoginUserView.as_view(),name="login"),
    path('profile_picture/<int:id>/',UpdateProfilePictureView.as_view(),name="profile_picture"),
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
    path('genres/',GetAllGenresView.as_view(), name="genres"),
    path('yourbooks/',GetOwnBooksView.as_view(), name="yourbooks"),

    #jwt token 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]