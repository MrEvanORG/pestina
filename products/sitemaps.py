from django.contrib.sitemaps import Sitemap
from .models import Product ,BlogPost , BlogCategories
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return ['home','products','blog','about-us']

    def location(self, item):
        return reverse(item)

class blogCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        return BlogCategories.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
    
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    def items(self):
        return Product.objects.filter(is_confirmed=True)

    def lastmod(self, obj):
        return obj.upload_time

    def location(self, obj):
        return obj.get_absolute_url()
    
class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_confirmed=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()

