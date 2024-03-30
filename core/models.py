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
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, default="profile_pictures/user.png")
    username = models.CharField(max_length=100,unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    genre = models.ManyToManyField(Genre,blank=True)
    otp = models.CharField(max_length=4, null=True)
    is_verified = models.BooleanField(default=False)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

'''user model'''



class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, null = False)
    author = models.CharField(max_length = 100,null = False)
    is_traded = models.BooleanField(default=False)
    genre = models.ForeignKey(Genre,blank=True, null=False, on_delete = models.DO_NOTHING)
    upload_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="book_images/", null = False)

    def __str__(self):
        return self.title
    
class Report(models.Model):
    class ReportType(models.TextChoices):
        SPAM = 'SP', 'Spam'
        INAPPROPRIATE_CONTENT = 'IC', 'Inappropriate Content'
        DIDNOT_APPEAR = "DA", "Didnot Appear"
        FAKE_BOOK = "FB", "Fake Book"

    reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reports_submitted')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    type = models.CharField(max_length=2, choices=ReportType.choices)
    report_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.reported_by} to {self.reported_user}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  

    def __str__(self):
        return f"{self.user.email} liked {self.book.title}"
    
class TradeRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "P", "Pending"
        ACCEPTED = "A", "Accepted"
        REJECTED = "R", "Rejected"
        INVALID = "I", "Invalid"
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_requests')
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requested_trade_requests')
    offered_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offered_trade_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    seen = models.BooleanField(default=False)







class Notification(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')
    message = models.TextField()
    image = models.ImageField(upload_to="notifications/", null = False)
