from django.urls import path
from core.views import RegisterUserView,ShowUsersView,UploadProfilePictureView

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),
    path('profile_picture/<int:id>/',UploadProfilePictureView.as_view(),name="profile_picture"),


]