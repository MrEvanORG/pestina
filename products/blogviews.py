#-------------------------------------------------#
from django.shortcuts import render, get_object_or_404
from .models import BlogPost , BlogCategories
from django.core.paginator import Paginator
#--------------------------------------------------#
def extract_post_preview(post):
    paragraph = None
    for block in post.content_blocks:
        if block.get("type") == "paragraph" and not paragraph:
            paragraph = block.get("text")
        if paragraph:
            break
    return {'paragraph': paragraph}
#--------------------------------------------------#
def blog_index(request):
    categories = BlogCategories.objects.all()
    return render(request, 'blog-pages/blog_index.html', {
    'ctgs': categories
    })

#--------------------------------------------------#
def blog_category(request, category_slug):
    ctg = get_object_or_404(BlogCategories,slug=category_slug)
    posts = BlogPost.objects.filter(category=ctg).order_by('-created_at')

    pagin = Paginator(posts,6)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)

    for post in posts :
        preview = extract_post_preview(post)
        post.preview = preview

    return render(request, 'blog-pages/blog_in_category.html', {
        'prd':page_obj,
        'posts': posts,
        'category_slug': category_slug,
        'category_title': ctg.title,
    })
#--------------------------------------------------#
def blog_post_detail(request, category_slug, post_slug):
    ctg = get_object_or_404(BlogCategories,slug=category_slug)
    post = get_object_or_404(BlogPost, slug=post_slug, category=ctg)

    session_key = f"viewed_post_{post.id}" #calcualte views
    if not request.session.get(session_key,False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    return render(request, 'blog-pages/blog_post_detail.html', {
        'ctg' : ctg ,
        'post': post , 
    })

