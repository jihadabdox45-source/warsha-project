from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# تخصيص عنوان لوحة التحكم
admin.site.site_header = "Warsha - لوحة التحكم"
admin.site.site_title = "Warsha Admin"
admin.site.index_title = "مرحباً بك في لوحة تحكم Warsha"


# تخصيص إدارة المستخدمين
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'get_stats']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    def get_stats(self, obj):
        """عرض إحصائيات المستخدم"""
        from crafts.models import Comment, Rating, Favorite
        comments = Comment.objects.filter(user=obj).count()
        ratings = Rating.objects.filter(user=obj).count()
        favorites = Favorite.objects.filter(user=obj).count()
        return f"💬 {comments} | ⭐ {ratings} | ❤️ {favorites}"
    get_stats.short_description = 'النشاط'


# إعادة تسجيل نموذج المستخدم
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
