from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact/messages/', views.contact_messages, name='contact_messages'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    
    # Additional Pages
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('faq/', views.faq, name='faq'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('dashboard/crafts/', views.dashboard_crafts, name='dashboard_crafts'),
    path('dashboard/crafts/add/', views.dashboard_craft_add, name='dashboard_craft_add'),
    path('dashboard/crafts/<int:craft_id>/edit/', views.dashboard_craft_edit, name='dashboard_craft_edit'),
    path('dashboard/crafts/<int:craft_id>/delete/', views.dashboard_craft_delete, name='dashboard_craft_delete'),
    path('dashboard/comments/', views.dashboard_comments, name='dashboard_comments'),
    path('dashboard/regions/', views.dashboard_regions, name='dashboard_regions'),
    path('dashboard/regions/add/', views.dashboard_region_add, name='dashboard_region_add'),
    path('dashboard/regions/<int:region_id>/edit/', views.dashboard_region_edit, name='dashboard_region_edit'),
    path('dashboard/regions/<int:region_id>/delete/', views.dashboard_region_delete, name='dashboard_region_delete'),
    path('dashboard/messages/', views.dashboard_messages, name='dashboard_messages'),
    
    # Dashboard Actions
    path('dashboard/comment/<int:comment_id>/approve/', views.dashboard_comment_approve, name='dashboard_comment_approve'),
    path('dashboard/comment/<int:comment_id>/delete/', views.dashboard_comment_delete, name='dashboard_comment_delete'),
    path('dashboard/message/<int:message_id>/mark-read/', views.dashboard_message_mark_read, name='dashboard_message_mark_read'),
    path('dashboard/message/<int:message_id>/delete/', views.dashboard_message_delete, name='dashboard_message_delete'),
]