from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from products.views import login_page , unknown_error
from products.admin import farmer_admin_site
from django.shortcuts import redirect
# site map --------------------------------
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap , StaticViewSitemap , BlogPostSitemap , blogCategorySitemap , ResumeSiteMap
from django.views.generic import TemplateView

sitemaps = {
    'static': StaticViewSitemap,
    'resume':ResumeSiteMap,
    'products': ProductSitemap,
    'blog_category':blogCategorySitemap,
    'blog_Post': BlogPostSitemap,
    }

def redirect_farmer_login(request):
    return redirect(login_page)


urlpatterns = [
    path('dashboard/login/',redirect_farmer_login),
    path('dashboard/', farmer_admin_site.urls,name='farmer-dashboard'),
    path('admin_jan_ammat_ino_be_kasi_nade/', admin.site.urls),
    path('',include('products.urls')),
    path('blog/',include('products.blogurls')),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

handler404 = 'products.views.custom_404'
handler500 = lambda request: unknown_error(request, status_code=500)
handler403 = lambda request, exception: unknown_error(request, exception, status_code=403)
handler400 = lambda request, exception: unknown_error(request, exception, status_code=400)
handler405 = lambda request, exception: unknown_error(request, exception, status_code=405)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
