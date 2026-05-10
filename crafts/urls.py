from django.urls import path
from . import views

app_name = 'crafts'

urlpatterns = [
    path('', views.all_crafts, name='all_crafts'),
    path('search/', views.search, name='search'),
    path('craft/<int:craft_id>/', views.craft_detail, name='craft_detail'),
    path('region/<str:region_name>/', views.region_detail, name='region_detail'),

    # Comments and Ratings
    path('craft/<int:craft_id>/comment/', views.add_comment, name='add_comment'),
    path('craft/<int:craft_id>/rating/', views.add_rating, name='add_rating'),
    path('craft/<int:craft_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Regions
    path('riyadh/', views.riyadh, name='riyadh'),
    path('makkah/', views.makkah, name='makkah'),
    path('madinah/', views.madinah, name='madinah'),
    path('asir/', views.asir, name='asir'),
    path('qassim/', views.qassim, name='qassim'),
    path('eastern/', views.eastern, name='eastern'),
    path('tabuk/', views.tabuk, name='tabuk'),
]