from django.urls import path
from core.views import RegisterUserView,ShowUsersView

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),

]