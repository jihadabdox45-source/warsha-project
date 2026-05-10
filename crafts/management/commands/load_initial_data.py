from django.core.management.base import BaseCommand
from crafts.models import Region, Craft, RegionEvent, RegionImage
from django.contrib.auth.models import User
import json
import os

class Command(BaseCommand):
    help = 'Load initial data from warsha_data.json'

    def handle(self, *args, **options):
        # Get the path to warsha_data.json
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        json_file = os.path.join(base_dir, 'warsha_data.json')
        
        self.stdout.write(self.style.SUCCESS(f'Loading data from {json_file}...'))
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stdout.write(self.style.SUCCESS(f'Found {len(data)} records\n'))
        
        # Import Users
        self.stdout.write('Importing Users...')
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
                user.set_password('warsha2024')  # Default password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {user.username}'))
            else:
                self.stdout.write(f'  - User exists: {user.username}')
        
        # Import Regions
        self.stdout.write('\nImporting Regions...')
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
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created region: {region.name}'))
            else:
                self.stdout.write(f'  - Region exists: {region.name}')
        
        # Import Region Events
        self.stdout.write('\nImporting Region Events...')
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
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created event: {event.name}'))
            except Region.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ! Region not found for event'))
        
        # Import Region Images
        self.stdout.write('\nImporting Region Images...')
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
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created image for: {region.name}'))
            except Region.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ! Region not found for image'))
        
        # Import Crafts
        self.stdout.write('\nImporting Crafts...')
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
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created craft: {craft.name}'))
                else:
                    self.stdout.write(f'  - Craft exists: {craft.name}')
            except Region.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ! Region not found for craft'))
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✓ Data import completed!'))
        self.stdout.write('='*60)
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Regions: {Region.objects.count()}')
        self.stdout.write(f'Events: {RegionEvent.objects.count()}')
        self.stdout.write(f'Images: {RegionImage.objects.count()}')
        self.stdout.write(f'Crafts: {Craft.objects.count()}')
        self.stdout.write('='*60)
        self.stdout.write(self.style.WARNING('\n⚠️  Default password for users: warsha2024'))
        self.stdout.write(self.style.WARNING('Please change it from /admin\n'))
