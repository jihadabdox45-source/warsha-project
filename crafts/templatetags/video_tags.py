import re
from django import template

register = template.Library()


@register.filter
def youtube_id(url):
    if not url:
        return None
    
    patterns = [
        r'(?:youtube(?:-nocookie)?\.com\/watch\?v=|youtu\.be\/|youtube(?:-nocookie)?\.com\/embed\/)([^&\n?#]+)',
        r'youtube(?:-nocookie)?\.com\/v\/([^&\n?#]+)',
        r'youtube(?:-nocookie)?\.com\/embed\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


@register.filter
def youtube_embed_url(url):
    video_id = youtube_id(url)
    if video_id:
        return f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1&rel=0&modestbranding=1&playsinline=1"
    return url


@register.filter
def youtube_thumbnail(url, quality='hqdefault'):
    video_id = youtube_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
    return None


@register.inclusion_tag('crafts/includes/video_player.html')
def video_player(video_url, title="Video"):
    vid_id = youtube_id(video_url)
    return {
        'video_url': video_url,
        'video_id': vid_id,
        'embed_url': youtube_embed_url(video_url),
        'thumbnail_hq': f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg" if vid_id else None,
        'thumbnail_max': f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg" if vid_id else None,
        'title': title
    }