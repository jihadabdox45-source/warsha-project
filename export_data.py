#!/usr/bin/env python
"""
سكريبت لتصدير البيانات من SQLite إلى JSON
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warsha_project.settings')
django.setup()

from django.core import serializers
from crafts.models import Region, Craft, RegionEvent, RegionImage, Comment, Rating, Favorite
from core.models import ContactMessage
from django.contrib.auth.models import User
import json

def export_data():
    data = []
    
    # Export Users (without passwords for security)
    print("Exporting Users...")
    users = User.objects.all()
    for user in users:
        data.append({
            'model': 'auth.user',
            'pk': user.pk,
            'fields': {
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),
            }
        })
    
    # Export Regions
    print("Exporting Regions...")
    regions = Region.objects.all()
    for region in regions:
        data.append({
            'model': 'crafts.region',
            'pk': region.pk,
            'fields': {
                'name': region.name,
                'slug': region.slug,
                'tagline': region.tagline,
                'brief': region.brief,
                'top_attraction': region.top_attraction,
                'history': region.history,
                'video_url': region.video_url,
                'created_at': region.created_at.isoformat(),
                'updated_at': region.updated_at.isoformat(),
            }
        })
    
    # Export Region Events
    print("Exporting Region Events...")
    events = RegionEvent.objects.all()
    for event in events:
        data.append({
            'model': 'crafts.regionevent',
            'pk': event.pk,
            'fields': {
                'region': event.region_id,
                'name': event.name,
                'order': event.order,
            }
        })
    
    # Export Region Images
    print("Exporting Region Images...")
    images = RegionImage.objects.all()
    for image in images:
        data.append({
            'model': 'crafts.regionimage',
            'pk': image.pk,
            'fields': {
                'region': image.region_id,
                'image': image.image,
                'order': image.order,
            }
        })
    
    # Export Crafts
    print("Exporting Crafts...")
    crafts = Craft.objects.all()
    for craft in crafts:
        data.append({
            'model': 'crafts.craft',
            'pk': craft.pk,
            'fields': {
                'name': craft.name,
                'slug': craft.slug,
                'region': craft.region_id,
                'description': craft.description,
                'image': craft.image,
                'is_featured': craft.is_featured,
                'created_at': craft.created_at.isoformat(),
                'updated_at': craft.updated_at.isoformat(),
            }
        })
    
    # Save to file
    print("Saving to file...")
    with open('warsha_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم تصدير {len(data)} سجل بنجاح!")
    print(f"   - Users: {users.count()}")
    print(f"   - Regions: {regions.count()}")
    print(f"   - Events: {events.count()}")
    print(f"   - Images: {images.count()}")
    print(f"   - Crafts: {crafts.count()}")
    print(f"\nالملف: warsha_data.json")

if __name__ == '__main__':
    export_data()
