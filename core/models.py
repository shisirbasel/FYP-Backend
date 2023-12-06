from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class Genre(models.Model):
    name = models.CharField(max_length=100,unique=True, verbose_name="Genre")
    
    def __str__(self):
        return self.name
    
'''user model'''
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, default=None)
    username = models.CharField(max_length=100)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    genre = models.ManyToManyField(Genre,blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

'''user model'''

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_traded = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre,blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="book_images/")

    def __str__(self):
        return self.title