from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Region, RegionEvent, RegionImage, Craft, Comment, Rating, Favorite


class RegionEventInline(TranslationTabularInline):
    model = RegionEvent
    extra = 1


class RegionImageInline(admin.TabularInline):
    model = RegionImage
    extra = 1


@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'tagline', 'created_at']
    search_fields = ['name', 'name_ar', 'name_en', 'tagline', 'tagline_ar', 'tagline_en', 'brief']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RegionEventInline, RegionImageInline]
    list_filter = ['created_at']
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Craft)
class CraftAdmin(TranslationAdmin):
    list_display = ['name', 'region', 'is_featured', 'get_rating', 'get_comments', 'created_at']
    search_fields = ['name', 'name_ar', 'name_en', 'description', 'description_ar', 'description_en']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['region', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    
    def get_rating(self, obj):
        return f"{obj.get_average_rating()}★ ({obj.get_rating_count()})"
    get_rating.short_description = 'Rating'
    
    def get_comments(self, obj):
        return obj.get_comments_count()
    get_comments.short_description = 'Comments'
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'craft', 'text_preview', 'is_approved', 'created_at']
    search_fields = ['user__username', 'craft__name', 'text']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'craft', 'stars', 'created_at']
    search_fields = ['user__username', 'craft__name']
    list_filter = ['stars', 'created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'craft', 'created_at']
    search_fields = ['user__username', 'craft__name']
    list_filter = ['created_at']