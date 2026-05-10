from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from .forms import ContactForm, UserRegistrationForm, UserLoginForm
from .models import ContactMessage
from crafts.models import Favorite, Comment, Rating, Craft, Region


def home(request):
    return render(request, 'core/home.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # حفظ الرسالة في قاعدة البيانات
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            
            # إضافة رسالة نجاح
            messages.success(request, 'Thank you! Your message has been sent successfully. We will get back to you soon.')
            
            # إعادة التوجيه لتجنب إعادة إرسال النموذج
            return redirect('core:contact')
        else:
            # إضافة رسالة خطأ
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form
    })


@login_required
def contact_messages(request):
    messages_list = ContactMessage.objects.all()
    
    return render(request, 'core/contact_messages.html', {
        'messages_list': messages_list
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! Your account has been created successfully.')
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'core:home')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile(request):
    from crafts.models import Favorite, Comment, Rating
    
    # حساب الإحصائيات
    favorites_count = Favorite.objects.filter(user=request.user).count()
    comments_count = Comment.objects.filter(user=request.user).count()
    ratings_count = Rating.objects.filter(user=request.user).count()
    
    # الحصول على الحرف المفضلة
    favorite_crafts = Favorite.objects.filter(user=request.user).select_related('craft', 'craft__region')[:6]
    
    # الحصول على آخر التعليقات
    recent_comments = Comment.objects.filter(user=request.user).select_related('craft')[:5]
    
    return render(request, 'core/profile.html', {
        'favorites_count': favorites_count,
        'comments_count': comments_count,
        'ratings_count': ratings_count,
        'favorite_crafts': favorite_crafts,
        'recent_comments': recent_comments,
    })


@login_required
def favorites(request):
    from crafts.models import Favorite
    
    # الحصول على جميع الحرف المفضلة
    favorites_list = Favorite.objects.filter(user=request.user).select_related('craft', 'craft__region').order_by('-created_at')
    
    # الفلترة حسب المنطقة
    region_filter = request.GET.get('region', '')
    if region_filter:
        favorites_list = favorites_list.filter(craft__region__slug=region_filter)
    
    # الترتيب
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'name':
        favorites_list = favorites_list.order_by('craft__name')
    elif sort_by == 'rating':
        from django.db.models import Avg
        favorites_list = favorites_list.annotate(avg_rating=Avg('craft__ratings__stars')).order_by('-avg_rating')
    elif sort_by == 'oldest':
        favorites_list = favorites_list.order_by('created_at')
    # default: recent (already ordered by -created_at)
    
    # Pagination
    paginator = Paginator(favorites_list, 12)  # 12 حرفة في كل صفحة
    page = request.GET.get('page')
    
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        favorites = paginator.page(1)
    except EmptyPage:
        favorites = paginator.page(paginator.num_pages)
    
    # الحصول على قائمة المناطق للفلترة
    regions = Region.objects.all()
    
    return render(request, 'core/favorites.html', {
        'favorites': favorites,
        'regions': regions,
        'region_filter': region_filter,
        'sort_by': sort_by,
    })


# ===== لوحة التحكم المخصصة =====

@staff_member_required
def dashboard(request):
    
    # إحصائيات عامة
    total_users = User.objects.count()
    total_crafts = Craft.objects.count()
    total_regions = Region.objects.count()
    total_comments = Comment.objects.filter(is_approved=True).count()
    total_ratings = Rating.objects.count()
    total_favorites = Favorite.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    
    # المستخدمون الجدد (آخر 7 أيام)
    week_ago = timezone.now() - timedelta(days=7)
    new_users = User.objects.filter(date_joined__gte=week_ago).count()
    
    # الحرف الأكثر تقييماً
    top_rated_crafts = Craft.objects.annotate(
        avg_rating=Avg('ratings__stars'),
        rating_count=Count('ratings')
    ).filter(rating_count__gt=0).order_by('-avg_rating', '-rating_count')[:5]
    
    # الحرف الأكثر تفضيلاً
    most_favorited_crafts = Craft.objects.annotate(
        favorites_count=Count('favorited_by')
    ).filter(favorites_count__gt=0).order_by('-favorites_count')[:5]
    
    # آخر التعليقات
    recent_comments = Comment.objects.select_related('user', 'craft').order_by('-created_at')[:10]
    
    # آخر المستخدمين المسجلين
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    context = {
        'total_users': total_users,
        'total_crafts': total_crafts,
        'total_regions': total_regions,
        'total_comments': total_comments,
        'total_ratings': total_ratings,
        'total_favorites': total_favorites,
        'pending_comments': pending_comments,
        'new_users': new_users,
        'top_rated_crafts': top_rated_crafts,
        'most_favorited_crafts': most_favorited_crafts,
        'recent_comments': recent_comments,
        'recent_users': recent_users,
    }
    
    return render(request, 'core/dashboard/index.html', context)


@staff_member_required
def dashboard_users(request):
    users_list = User.objects.annotate(
        comments_count=Count('comments'),
        ratings_count=Count('ratings'),
        favorites_count=Count('favorites')
    ).order_by('-date_joined')
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = users_list.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users_list, 20)  # 20 مستخدم في كل صفحة
    page = request.GET.get('page')
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    
    return render(request, 'core/dashboard/users.html', context)


@staff_member_required
def dashboard_crafts(request):
    crafts_list = Craft.objects.select_related('region').annotate(
        avg_rating=Avg('ratings__stars'),
        rating_count=Count('ratings'),
        comments_count=Count('comments'),
        favorites_count=Count('favorited_by')
    ).order_by('-created_at')
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        crafts_list = crafts_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(region__name__icontains=search_query)
        )
    
    # الفلترة حسب المنطقة
    region_filter = request.GET.get('region', '')
    if region_filter:
        crafts_list = crafts_list.filter(region__slug=region_filter)
    
    # Pagination
    paginator = Paginator(crafts_list, 20)  # 20 حرفة في كل صفحة
    page = request.GET.get('page')
    
    try:
        crafts = paginator.page(page)
    except PageNotAnInteger:
        crafts = paginator.page(1)
    except EmptyPage:
        crafts = paginator.page(paginator.num_pages)
    
    regions = Region.objects.all()
    
    context = {
        'crafts': crafts,
        'regions': regions,
        'search_query': search_query,
        'region_filter': region_filter,
    }
    
    return render(request, 'core/dashboard/crafts.html', context)


@staff_member_required
def dashboard_comments(request):
    comments_list = Comment.objects.select_related('user', 'craft').order_by('-created_at')
    
    # الفلترة حسب الحالة
    status_filter = request.GET.get('status', '')
    if status_filter == 'approved':
        comments_list = comments_list.filter(is_approved=True)
    elif status_filter == 'pending':
        comments_list = comments_list.filter(is_approved=False)
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        comments_list = comments_list.filter(
            Q(text__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(craft__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(comments_list, 20)  # 20 تعليق في كل صفحة
    page = request.GET.get('page')
    
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context = {
        'comments': comments,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'core/dashboard/comments.html', context)


@staff_member_required
def dashboard_regions(request):
    regions = Region.objects.annotate(
        crafts_count=Count('crafts')
    ).order_by('name')
    
    context = {
        'regions': regions,
    }
    
    return render(request, 'core/dashboard/regions.html', context)


@staff_member_required
def dashboard_messages(request):
    messages_queryset = ContactMessage.objects.order_by('-created_at')
    
    # الفلترة حسب الحالة
    status_filter = request.GET.get('status', '')
    if status_filter == 'read':
        messages_queryset = messages_queryset.filter(is_read=True)
    elif status_filter == 'unread':
        messages_queryset = messages_queryset.filter(is_read=False)
    
    # Pagination
    paginator = Paginator(messages_queryset, 20)  # 20 رسالة في كل صفحة
    page = request.GET.get('page')
    
    try:
        messages_list = paginator.page(page)
    except PageNotAnInteger:
        messages_list = paginator.page(1)
    except EmptyPage:
        messages_list = paginator.page(paginator.num_pages)
    
    context = {
        'messages_list': messages_list,
        'status_filter': status_filter,
    }
    
    return render(request, 'core/dashboard/messages.html', context)


@staff_member_required
def dashboard_comment_approve(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.is_approved = True
        comment.save()
        messages.success(request, 'Comment approved successfully.')
    return redirect('core:dashboard_comments')


@staff_member_required
def dashboard_comment_delete(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('core:dashboard_comments')


@staff_member_required
def dashboard_message_mark_read(request, message_id):
    if request.method == 'POST':
        message = ContactMessage.objects.get(id=message_id)
        message.is_read = True
        message.save()
        messages.success(request, 'Message marked as read.')
    return redirect('core:dashboard_messages')


@staff_member_required
def dashboard_message_delete(request, message_id):
    if request.method == 'POST':
        message = ContactMessage.objects.get(id=message_id)
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('core:dashboard_messages')



@staff_member_required
def dashboard_craft_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        region_id = request.POST.get('region')
        description = request.POST.get('description')
        image = request.POST.get('image')
        is_featured = request.POST.get('is_featured') == 'on'
        
        Craft.objects.create(
            name=name,
            slug=slug,
            region_id=region_id,
            description=description,
            image=image,
            is_featured=is_featured
        )
        messages.success(request, 'Craft added successfully.')
        return redirect('core:dashboard_crafts')
    
    regions = Region.objects.all()
    return render(request, 'core/dashboard/craft_form.html', {
        'regions': regions,
        'action': 'add'
    })


@staff_member_required
def dashboard_craft_edit(request, craft_id):
    craft = Craft.objects.get(id=craft_id)
    
    if request.method == 'POST':
        craft.name = request.POST.get('name')
        craft.slug = request.POST.get('slug')
        craft.region_id = request.POST.get('region')
        craft.description = request.POST.get('description')
        craft.image = request.POST.get('image')
        craft.is_featured = request.POST.get('is_featured') == 'on'
        craft.save()
        
        messages.success(request, 'Craft updated successfully.')
        return redirect('core:dashboard_crafts')
    
    regions = Region.objects.all()
    return render(request, 'core/dashboard/craft_form.html', {
        'craft': craft,
        'regions': regions,
        'action': 'edit'
    })


@staff_member_required
def dashboard_craft_delete(request, craft_id):
    if request.method == 'POST':
        craft = Craft.objects.get(id=craft_id)
        craft.delete()
        messages.success(request, 'Craft deleted successfully.')
    return redirect('core:dashboard_crafts')



@staff_member_required
def dashboard_region_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        tagline = request.POST.get('tagline')
        brief = request.POST.get('brief')
        top_attraction = request.POST.get('top_attraction')
        history = request.POST.get('history')
        video_url = request.POST.get('video_url')
        
        region = Region.objects.create(
            name=name,
            slug=slug,
            tagline=tagline,
            brief=brief,
            top_attraction=top_attraction,
            history=history,
            video_url=video_url if video_url else None
        )
        
        # إضافة الفعاليات
        events = request.POST.getlist('events[]')
        for i, event_name in enumerate(events):
            if event_name.strip():
                from crafts.models import RegionEvent
                RegionEvent.objects.create(
                    region=region,
                    name=event_name,
                    order=i
                )
        
        # إضافة الصور
        images = request.POST.getlist('images[]')
        for i, image_path in enumerate(images):
            if image_path.strip():
                from crafts.models import RegionImage
                RegionImage.objects.create(
                    region=region,
                    image=image_path,
                    order=i
                )
        
        messages.success(request, 'Region added successfully.')
        return redirect('core:dashboard_regions')
    
    return render(request, 'core/dashboard/region_form.html', {
        'action': 'add'
    })


@staff_member_required
def dashboard_region_edit(request, region_id):
    region = Region.objects.get(id=region_id)
    
    if request.method == 'POST':
        region.name = request.POST.get('name')
        region.slug = request.POST.get('slug')
        region.tagline = request.POST.get('tagline')
        region.brief = request.POST.get('brief')
        region.top_attraction = request.POST.get('top_attraction')
        region.history = request.POST.get('history')
        region.video_url = request.POST.get('video_url') if request.POST.get('video_url') else None
        region.save()
        
        # تحديث الفعاليات
        from crafts.models import RegionEvent
        region.events.all().delete()
        events = request.POST.getlist('events[]')
        for i, event_name in enumerate(events):
            if event_name.strip():
                RegionEvent.objects.create(
                    region=region,
                    name=event_name,
                    order=i
                )
        
        # تحديث الصور
        from crafts.models import RegionImage
        region.images.all().delete()
        images = request.POST.getlist('images[]')
        for i, image_path in enumerate(images):
            if image_path.strip():
                RegionImage.objects.create(
                    region=region,
                    image=image_path,
                    order=i
                )
        
        messages.success(request, 'Region updated successfully.')
        return redirect('core:dashboard_regions')
    
    return render(request, 'core/dashboard/region_form.html', {
        'region': region,
        'action': 'edit'
    })


@staff_member_required
def dashboard_region_delete(request, region_id):
    if request.method == 'POST':
        region = Region.objects.get(id=region_id)
        region.delete()
        messages.success(request, 'Region deleted successfully.')
    return redirect('core:dashboard_regions')


# ===== الصفحات الإضافية =====

def about(request):
    return render(request, 'core/about.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def faq(request):
    """صفحة الأسئلة الشائعة"""
    return render(request, 'core/faq.html')
