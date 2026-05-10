from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المنطقة')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='الرابط')
    tagline = models.CharField(max_length=200, verbose_name='الشعار')
    brief = models.TextField(verbose_name='نبذة مختصرة')
    top_attraction = models.CharField(max_length=200, verbose_name='أبرز معلم')
    history = models.TextField(verbose_name='التاريخ')
    video_url = models.URLField(blank=True, null=True, verbose_name='رابط الفيديو')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'منطقة'
        verbose_name_plural = 'المناطق'
        ordering = ['name']

    def __str__(self):
        return self.name


class RegionEvent(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='events', verbose_name='المنطقة')
    name = models.CharField(max_length=200, verbose_name='اسم الفعالية')
    order = models.IntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        verbose_name = 'فعالية'
        verbose_name_plural = 'الفعاليات'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.region.name} - {self.name}"


class RegionImage(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='images', verbose_name='المنطقة')
    image = models.CharField(max_length=300, verbose_name='مسار الصورة')
    order = models.IntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        verbose_name = 'صورة المنطقة'
        verbose_name_plural = 'صور المناطق'
        ordering = ['order']

    def __str__(self):
        return f"{self.region.name} - صورة {self.order}"


class Craft(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم الحرفة')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='الرابط')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='crafts', verbose_name='المنطقة')
    description = models.TextField(verbose_name='الوصف')
    image = models.CharField(max_length=300, verbose_name='مسار الصورة')
    is_featured = models.BooleanField(default=False, verbose_name='حرفة مميزة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'حرفة'
        verbose_name_plural = 'الحرف اليدوية'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.stars for r in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        return self.ratings.count()

    def get_comments_count(self):
        return self.comments.filter(is_approved=True).count()


class Comment(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name='comments', verbose_name='الحرفة')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='المستخدم')
    text = models.TextField(verbose_name='التعليق')
    is_approved = models.BooleanField(default=True, verbose_name='موافق عليه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'التعليقات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.craft.name}"


class Rating(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name='ratings', verbose_name='الحرفة')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='المستخدم')
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='عدد النجوم'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
        unique_together = ['craft', 'user']  # مستخدم واحد يقيم حرفة واحدة مرة واحدة
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.craft.name} - {self.stars}★"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='المستخدم')
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='الحرفة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')

    class Meta:
        verbose_name = 'مفضلة'
        verbose_name_plural = 'المفضلات'
        unique_together = ['user', 'craft']  # مستخدم واحد يضيف حرفة واحدة مرة واحدة
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.craft.name}"