from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Region, Craft, Comment, Rating, Favorite
from .forms import CommentForm, RatingForm


def all_crafts(request):
    crafts_list = Craft.objects.select_related('region').all()
    
    # Pagination
    paginator = Paginator(crafts_list, 12)  # 12 حرفة في كل صفحة
    page = request.GET.get('page')
    
    try:
        crafts = paginator.page(page)
    except PageNotAnInteger:
        crafts = paginator.page(1)
    except EmptyPage:
        crafts = paginator.page(paginator.num_pages)
    
    return render(request, 'crafts/all_crafts.html', {
        'crafts': crafts
    })


def craft_detail(request, craft_id):
    craft = get_object_or_404(Craft, id=craft_id)
    comments_list = craft.comments.filter(is_approved=True).select_related('user')
    
    # Pagination للتعليقات
    paginator = Paginator(comments_list, 10)  # 10 تعليقات في كل صفحة
    page = request.GET.get('page')
    
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    # التحقق من تقييم المستخدم
    user_rating = None
    user_has_favorited = False
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(craft=craft, user=request.user).first()
        user_has_favorited = Favorite.objects.filter(craft=craft, user=request.user).exists()
    
    # معالجة نموذج التعليق
    if request.method == 'POST' and request.user.is_authenticated:
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.craft = craft
                comment.user = request.user
                comment.save()
                messages.success(request, 'Your comment has been added successfully!')
                return redirect('crafts:craft_detail', craft_id=craft_id)
        
        elif 'rating_submit' in request.POST:
            stars = request.POST.get('stars')
            if stars:
                Rating.objects.update_or_create(
                    craft=craft,
                    user=request.user,
                    defaults={'stars': int(stars)}
                )
                messages.success(request, 'Your rating has been saved!')
                return redirect('crafts:craft_detail', craft_id=craft_id)
    
    comment_form = CommentForm()
    
    return render(request, 'crafts/craft_detail.html', {
        'craft': craft,
        'comments': comments,
        'comment_form': comment_form,
        'user_rating': user_rating,
        'user_has_favorited': user_has_favorited,
    })


@login_required
def add_comment(request, craft_id):
    craft = get_object_or_404(Craft, id=craft_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.craft = craft
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('crafts:craft_detail', craft_id=craft_id)


@login_required
def add_rating(request, craft_id):
    craft = get_object_or_404(Craft, id=craft_id)
    
    if request.method == 'POST':
        stars = request.POST.get('stars')
        if stars and 1 <= int(stars) <= 5:
            Rating.objects.update_or_create(
                craft=craft,
                user=request.user,
                defaults={'stars': int(stars)}
            )
            messages.success(request, 'Your rating has been saved!')
        else:
            messages.error(request, 'Please select a valid rating.')
    
    return redirect('crafts:craft_detail', craft_id=craft_id)


@login_required
def toggle_favorite(request, craft_id):
    craft = get_object_or_404(Craft, id=craft_id)
    
    favorite, created = Favorite.objects.get_or_create(
        craft=craft,
        user=request.user
    )
    
    if not created:
        favorite.delete()
        messages.success(request, 'Removed from favorites!')
    else:
        messages.success(request, 'Added to favorites!')
    
    return redirect('crafts:craft_detail', craft_id=craft_id)


def region_detail(request, region_name):
    region = get_object_or_404(Region, slug=region_name)
    crafts_list = region.crafts.all()
    
    # Pagination
    paginator = Paginator(crafts_list, 12)  # 12 حرفة في كل صفحة
    page = request.GET.get('page')
    
    try:
        related_crafts = paginator.page(page)
    except PageNotAnInteger:
        related_crafts = paginator.page(1)
    except EmptyPage:
        related_crafts = paginator.page(paginator.num_pages)

    return render(request, 'crafts/region_detail.html', {
        'region': region,
        'region_name': region_name,
        'related_crafts': related_crafts
    })


def riyadh(request):
    region = get_object_or_404(Region, slug='riyadh')
    return render(request, 'crafts/riyadh.html', {
        'region': region
    })


def makkah(request):
    region = get_object_or_404(Region, slug='makkah')
    return render(request, 'crafts/makkah.html', {
        'region': region
    })


def madinah(request):
    region = get_object_or_404(Region, slug='madinah')
    return render(request, 'crafts/madinah.html', {
        'region': region
    })


def asir(request):
    region = get_object_or_404(Region, slug='asir')
    return render(request, 'crafts/asir.html', {
        'region': region
    })


def qassim(request):
    region = get_object_or_404(Region, slug='qassim')
    return render(request, 'crafts/qassim.html', {
        'region': region
    })


def eastern(request):
    region = get_object_or_404(Region, slug='eastern')
    return render(request, 'crafts/eastern.html', {
        'region': region
    })


def tabuk(request):
    region = get_object_or_404(Region, slug='tabuk')
    return render(request, 'crafts/tabuk.html', {
        'region': region
    })


def search(request):
    query = request.GET.get('q', '')
    results_list = []

    if query:
        # البحث في الحرف
        crafts = Craft.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('region')
        
        for craft in crafts:
            results_list.append({
                'id': craft.id,
                'name': craft.name,
                'region': craft.region.slug,
                'description': craft.description,
                'image': craft.image,
            })

        # البحث في المناطق
        regions = Region.objects.filter(
            Q(name__icontains=query) | Q(brief__icontains=query)
        )
        
        for region in regions:
            first_image = region.images.first()
            results_list.append({
                'id': 0,
                'name': region.name,
                'region': region.slug,
                'description': region.brief,
                'image': first_image.image if first_image else '',
            })
    
    # Pagination
    paginator = Paginator(results_list, 12)  # 12 نتيجة في كل صفحة
    page = request.GET.get('page')
    
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'crafts/search.html', {
        'query': query,
        'results': results
    })