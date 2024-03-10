from django.contrib import admin
from .models import User, Book, Genre, Report, Like, TradeRequest, Author

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'author', 'is_traded', 'upload_date')
    search_fields = ('title', 'author__author')
    list_filter = ('is_traded', 'upload_date')

admin.site.register(Book, BookAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'reported_user', 'type', 'report_date')
    search_fields = ('reported_by__email', 'reported_user__email')
    list_filter = ('type', 'report_date')

admin.site.register(Report, ReportAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'liked_date')
    search_fields = ('user__email', 'book__title')
    list_filter = ('liked_date',)

admin.site.register(Like, LikeAdmin)

class TradeRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_book', 'offered_book', 'request_date', 'status')
    search_fields = ('user__email', 'requested_book__title', 'offered_book__title')
    list_filter = ('request_date', 'status')

admin.site.register(TradeRequest, TradeRequestAdmin)


admin.site.register(Author)