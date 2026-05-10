#!/usr/bin/env python
"""
سكريبت لاستيراد البيانات إلى قاعدة البيانات
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warsha_project.settings')
django.setup()

from crafts.models import Region, Craft, RegionEvent, RegionImage
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

def import_data():
    print("Loading data from warsha_data.json...")
    
    with open('warsha_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} records\n")
    
    # Import in order: Users -> Regions -> Events -> Images -> Crafts
    
    # 1. Import Users
    print("Importing Users...")
    users_data = [item for item in data if item['model'] == 'auth.user']
    for item in users_data:
        fields = item['fields']
        user, created = User.objects.get_or_create(
            username=fields['username'],
            defaults={
                'email': fields['email'],
                'is_staff': fields['is_staff'],
                'is_superuser': fields['is_superuser'],
                'is_active': fields['is_active'],
            }
        )
        if created:
            # Set a default password (user will need to reset)
            user.set_password('changeme123')
            user.save()
            print(f"  ✅ Created user: {user.username}")
        else:
            print(f"  ⏭️  User exists: {user.username}")
    
    # 2. Import Regions
    print("\nImporting Regions...")
    regions_data = [item for item in data if item['model'] == 'crafts.region']
    for item in regions_data:
        fields = item['fields']
        region, created = Region.objects.get_or_create(
            slug=fields['slug'],
            defaults={
                'name': fields['name'],
                'tagline': fields['tagline'],
                'brief': fields['brief'],
                'top_attraction': fields['top_attraction'],
                'history': fields['history'],
                'video_url': fields.get('video_url'),
            }
        )
        if created:
            print(f"  ✅ Created region: {region.name}")
        else:
            print(f"  ⏭️  Region exists: {region.name}")
    
    # 3. Import Region Events
    print("\nImporting Region Events...")
    events_data = [item for item in data if item['model'] == 'crafts.regionevent']
    for item in events_data:
        fields = item['fields']
        try:
            region = Region.objects.get(pk=fields['region'])
            event, created = RegionEvent.objects.get_or_create(
                region=region,
                name=fields['name'],
                defaults={'order': fields['order']}
            )
            if created:
                print(f"  ✅ Created event: {event.name}")
        except Region.DoesNotExist:
            print(f"  ⚠️  Region not found for event: {fields['name']}")
    
    # 4. Import Region Images
    print("\nImporting Region Images...")
    images_data = [item for item in data if item['model'] == 'crafts.regionimage']
    for item in images_data:
        fields = item['fields']
        try:
            region = Region.objects.get(pk=fields['region'])
            image, created = RegionImage.objects.get_or_create(
                region=region,
                image=fields['image'],
                defaults={'order': fields['order']}
            )
            if created:
                print(f"  ✅ Created image for: {region.name}")
        except Region.DoesNotExist:
            print(f"  ⚠️  Region not found for image")
    
    # 5. Import Crafts
    print("\nImporting Crafts...")
    crafts_data = [item for item in data if item['model'] == 'crafts.craft']
    for item in crafts_data:
        fields = item['fields']
        try:
            region = Region.objects.get(pk=fields['region'])
            craft, created = Craft.objects.get_or_create(
                slug=fields['slug'],
                defaults={
                    'name': fields['name'],
                    'region': region,
                    'description': fields['description'],
                    'image': fields['image'],
                    'is_featured': fields['is_featured'],
                }
            )
            if created:
                print(f"  ✅ Created craft: {craft.name}")
            else:
                print(f"  ⏭️  Craft exists: {craft.name}")
        except Region.DoesNotExist:
            print(f"  ⚠️  Region not found for craft: {fields['name']}")
    
    print("\n" + "="*60)
    print("✅ تم استيراد البيانات بنجاح!")
    print("="*60)
    print(f"Users: {User.objects.count()}")
    print(f"Regions: {Region.objects.count()}")
    print(f"Events: {RegionEvent.objects.count()}")
    print(f"Images: {RegionImage.objects.count()}")
    print(f"Crafts: {Craft.objects.count()}")
    print("="*60)
    print("\n⚠️  ملاحظة: كلمة المرور الافتراضية للمستخدمين: changeme123")
    print("يرجى تغييرها من لوحة التحكم /admin\n")

if __name__ == '__main__':
    import_data()
