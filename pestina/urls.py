"""
URL configuration for pestina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from products import views
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

urlpatterns = [

    path('',include('products.urls')),
    path('blog/',include('products.blogurls')),
    path('admin_jan_ammat_ino_be_kasi_nade/', admin.site.urls),

    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

handler404 = 'products.views.custom_404'
handler500 = lambda request: views.unknown_error(request, status_code=500)
handler403 = lambda request, exception: views.unknown_error(request, exception, status_code=403)
handler400 = lambda request, exception: views.unknown_error(request, exception, status_code=400)
handler405 = lambda request, exception: views.unknown_error(request, exception, status_code=405)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
