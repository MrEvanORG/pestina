from .models import SeoData
def seo_processor(request):
    path = request.path
    try:
        seo_data = SeoData.objects.get(path=path)
        return {"seo_title":seo_data.title,"seo_description":seo_data.meta_description}
    except:
        return {}