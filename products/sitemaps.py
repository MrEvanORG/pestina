from django.contrib.sitemaps import Sitemap
from .models import Product
from django.urls import reverse

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9


    def items(self):
        return Product.objects.filter(is_confirmed=True)

    def lastmod(self, obj):
        return obj.upload_time

    def location(self, obj):
        return obj.get_absolute_url()
    


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ['home', 'about-us', 'products']

    def location(self, item):
        return reverse(item)