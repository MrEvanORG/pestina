from products.views import *
from django.shortcuts import render
def blog(request):
    context = {'text':'وبلاگ پستینا در حال راه اندازی است پس از آن میتونید از مطالب این بخش استفاده کنید'}
    return render(request,'soon_page.html',context)