from django.urls import path
from core.views import RegisterUserView,ShowUsersView,UploadProfilePictureView, LoginUserView, AddBookView, \
            UpdateBookView,ShowBooksView,DeleteBookView

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name="register"),
    path('users/',ShowUsersView.as_view(),name="show_users"),
    path('login/',LoginUserView.as_view(),name="login"),
    path('profile_picture/<int:id>/',UploadProfilePictureView.as_view(),name="profile_picture"),
    path('add_book/',AddBookView.as_view(),name="add_book"),
    path('update_book/<int:id>/',UpdateBookView.as_view(),name="update_book"),
    path('show_books/',ShowBooksView.as_view(),name="show_books"),
    path('delete_book/<int:id>/',DeleteBookView.as_view(),name="delete_book"),
]