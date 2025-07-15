from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .addons import persian_slugify
from taggit.managers import TaggableManager
# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=20,verbose_name='نام کاربر')
    last_name = models.CharField(max_length=20,verbose_name='نام خانوادگی کاربر')
    phone_number = models.CharField(max_length=15,unique=True,verbose_name='شماره تلفن کاربر')
    is_verified = models.BooleanField(default=False,verbose_name='وضعیت تایید شدن شماره تلغن')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی کاربر هنگام ثبت نام')
    register_time = models.DateTimeField(auto_now=True,verbose_name='زمان ثبت نام')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):

    class ptype(models.TextChoices):
        AKBARI = "akbari","اکبری"
        FANDOGHI = "fandoghi","فندوقی"
        AHMADAGHAII = "ahmadaghaii","احمد آقایی"
        KALE_GHOOCHI = 'kaleghoochi','کله قوچی'
        SHAHPASAND = 'shahpasand','شاه پسند'
        SEPID = 'sefid','سفید'
        BADAMI = 'badami','بادامی'
        KHANJARI = 'khanjari','خنجری'
        MAKHLOOT = 'makhloot',' مخلوط'
        
    class pstatus(models.TextChoices):
        KHANDAN = 'khandan','خندان'
        DAHANBAST = 'dahanbast','دهن بست'
        ABKHANDAN = 'abkhandan','آب خندان'
        TARKIBI = 'tarkibi','ترکیبی'

    class pquality(models.TextChoices):
        D1 = 'd1','درجه یک'
        D2 = 'd2','درجه دو'
        D3 = 'd3','درجه سه'
        D4 = 'd4','درجه چهار'

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    id = models.AutoField(primary_key=True,verbose_name='آیدی محصول')

    photo = models.ImageField(verbose_name='عکس محصول',upload_to='prdphotos')
    kind = models.CharField(max_length=20,choices=ptype.choices,verbose_name='نوع پسته')
    status = models.CharField(max_length=20,choices=pstatus.choices,verbose_name='وضعیت محصول')
    ounce = models.PositiveIntegerField(verbose_name='انس محصول')
    quality = models.CharField(max_length=20,choices=pquality.choices,verbose_name='(کیفی) کیفیت محصول')
    price = models.DecimalField(max_digits=13,decimal_places=0,verbose_name='(تومان) قیمت محصول')
    show_inventory = models.BooleanField(default=True,verbose_name='وضعیت نمایش وزن محصول')
    inventory = models.FloatField(verbose_name='وزن محصول')
    min_order = models.FloatField(null=True,blank=True,verbose_name='حداقل سفارش (کیلوگرم - خالی برای بدون محدودیت)')
    max_order = models.FloatField(null=True,blank=True,verbose_name='حداکثر سفارش (کیلوگرم - خالی برای بدون محدودیت)')
    discription = models.CharField(max_length=500,null=True,blank=True,verbose_name='توضیحات بیشتر برای محصول')
    free_shipping = models.BooleanField(default=False,verbose_name='ارسال رایگان')
    shipping_cost = models.DecimalField(max_digits=13,null=True,blank=True,decimal_places=0,verbose_name='(تومان) هزینه ارسال')
    is_pestina_product = models.BooleanField(default=False,verbose_name='محصول پستینا')
    is_confirmed = models.BooleanField(default=False,verbose_name='وضعیت تایید شدن توسط ادمین')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی')
    upload_time = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت محصول')

    def save(self,*args,**kwargs):
        if self.free_shipping :
            self.shipping_cost = None
        super().save(*args,**kwargs)
    

    def get_absolute_url(self):
        return reverse("buy-product", args=[self.id])


    def __str__(self):
        return f"{self.kind} uploaded by {'admin' if self.is_pestina_product else self.user.first_name}"


# class RawData(models.Model):
#     user_logout_time = models.BigIntegerField(verbose_name='مدت زمان لاگین ماندن کاربر (به ثانیه)',default=2*60*60)
#     product_per_page = models.IntegerField(verbose_name='تعداد محصول قابل نمایش در هر صفحه',default=9)

#     minimum_gain_order = models.FloatField(verbose_name='کمترین مقدار قابل سفارش از هز محصولی (به کیلوگرم)',default=0.1)

#     max_post_gain = models.FloatField('بیشترین وزن قابل ارسال با پست (به کیلوگرم)',default=30)
#     max_post_cost = models.DecimalField(max_digits=13,decimal_places=0,verbose_name='بیشترین هزینه ارسال پست (به تومان)',)

#     max_tipax_gain = models.FloatField(verbose_name='بیشترین وزن قابل ارسال با تیپاکس (به کیلوگرم)')
#     max_tipax_cost = models.DecimalField(max_digits=13,decimal_places=0,verbose_name='بیشترین هزینه ارسال تیپاکس (به تومان)')

    

class Ticket(models.Model):
    class TicketType(models.TextChoices):
        FEEDBACK = "feedback","نظرات و پیشنهادات"
        PURCHASE = "purchase","درخواست خرید محصول"
        TECHNICAL = "technical","نقص فنی سایت"

    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,verbose_name='کاربر')

    ticket_id = models.AutoField(primary_key=True,verbose_name='شماره تیکت')
    buyer_namelastname = models.CharField(max_length=30,verbose_name='نام خریدار') #need to fill
    buyer_phone = models.CharField(max_length=20,verbose_name='شماره تلفن')
    ticket_type = models.CharField(max_length=20,choices=TicketType.choices,verbose_name='نوع تیکت')
    request_title = models.CharField(max_length=20,verbose_name='عنوان تیکت')
    request_discription = models.CharField(max_length=150,verbose_name='متن درخواست')
    ticket_time = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت تیکت')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='أیپی')

    def __str__(self):
        return f"{self.ticket_type} -> by {self.buyer_namelastname} {self.buyer_phone}"

class BuyTicket(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='شماره سفارش')
    name = models.CharField(max_length=30,verbose_name='نام خریدار')
    phone = models.CharField(max_length=20,verbose_name='شماره تلفن')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='محصول سفارش داده شده')
    gain = models.FloatField(verbose_name='مقدار (به کیلو)')
    price = models.FloatField(verbose_name='قیمت نهایی')
    post_code = models.BigIntegerField(verbose_name='کد پستی')
    address = models.CharField(max_length=1500,verbose_name='آدرس')
    buy_time = models.DateTimeField(auto_now=True,verbose_name='تاریخ سفارش')
    ip_address = models.GenericIPAddressField(null=True,blank=True,verbose_name='آیپی')

    def __str__(self):
        return self.name

class BlogCategories(models.Model):
    title = models.CharField(max_length=50,verbose_name='نام دسته بندی')
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True,verbose_name='اسلاگ (ساخن خودکار از روی اسم کتگوری)')
    discription = models.CharField(max_length=300,verbose_name='توضیحات دسته بندی')
    photo = models.ImageField(upload_to='blog-photos/covers-category/',verbose_name='کاور دسته بندی',blank=True,null=True)

    def save(self,*args,**kwargs):
        if not self.slug :
            self.slug = persian_slugify(self.title)
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    def post_count(self):
        return self.blogpost_set.count()
    
    def get_absolute_url(self):
        return reverse("blog_category", args=[self.slug])
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200,verbose_name='عنوان')
    auther = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,verbose_name='نویسنده')
    slug = models.SlugField(allow_unicode=True,unique=True, blank=True,)
    category = models.ForeignKey(BlogCategories,on_delete=models.SET_NULL,null=True,verbose_name='دسته بندی')
    content_blocks = models.JSONField(default=list,verbose_name='بلاک های محتوا')  
    cover_image = models.ImageField(upload_to='blog-photos/covers/',verbose_name='کاور پست')
    image1 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 1')
    image2 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 2')
    image3 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 3')
    image4 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 4')
    image5 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 5')
    image6 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 6')
    image7 = models.ImageField(upload_to='blog-photos/images/', blank=True, null=True,verbose_name='عکس 7')
    views = models.PositiveIntegerField(default=0)
    time_to_read = models.IntegerField(verbose_name='زمان تقریبی خواندن (به دقیقه)',default=3)
    tags = TaggableManager(blank=True,verbose_name='برچسب ها (با , جداکنید)')
    refrence_url = models.URLField(blank=True,null=True,verbose_name='لینک ارجاع')
    refrence_url_text = models.CharField(max_length=30,blank=True,null=True,verbose_name='متن ارجاع')
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False,verbose_name='وضعیت تایید شدن توسط ادمین')

    def save(self,*args,**kwargs):
        if not self.slug :
            self.slug = persian_slugify(self.title)
        super().save(*args,**kwargs)

    def get_image_by_name(self, name):
        return getattr(self, name, None)
    
    def get_absolute_url(self):
        return reverse("blog_post_detail", args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.title


