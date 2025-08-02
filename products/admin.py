from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from jsoneditor.forms import JSONEditor
from django.contrib.auth import get_user_model
from .models import SeoData , User , Product , Ticket , BuyTicket , BlogCategories , BlogPost , Resume , Education , WorkExperience , models


@admin.register(SeoData)
class SeoDataAdmin(admin.ModelAdmin):
    list_display = (
        "path",
        "title",
        "meta_description"
    )


User = get_user_model()
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_verified",
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'phone_number',  
            'province',      
            'city',          
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_verified',
            'groups',
            'user_permissions',
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = (
        "is_staff", 
        "is_superuser", 
        "is_active", 
        "groups", 
        "is_verified",
        "province", 
    )

    search_fields = (
        "username", 
        "first_name", 
        "last_name", 
        "email", 
        "phone_number",
    )

    ordering = ("-date_joined",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'kind',
        'status',
        'price',
        'inventory',
        'is_pestina_product',
        'is_confirmed'
    )
    list_filter = ('kind', 'status', 'quality', 'is_confirmed', 'is_pestina_product', 'free_shipping')
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'discription')
    ordering = ('-upload_time',)
    readonly_fields = ('ip_address', 'upload_time')
    autocomplete_fields = ('user',)
    list_editable = ('price', 'inventory', 'is_confirmed')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'kind', 'status', 'ounce', 'quality', 'photo')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'inventory', 'show_inventory', 'min_order', 'max_order')
        }),
        ('اطلاعات ارسال', {
            'fields': ('free_shipping', 'shipping_cost')
        }),
        ('وضعیت و توضیحات', {
            'fields': ('is_confirmed', 'is_pestina_product', 'discription')
        }),
        ('اطلاعات سیستم', {
            'fields': ('ip_address', 'upload_time'),
            'classes': ('collapse',)
        })
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_id',
        'ticket_type',
        'request_title',
        'buyer_namelastname',
        'buyer_phone',
        'ticket_time'
    )
    list_filter = ('ticket_type',)
    search_fields = ('ticket_id', 'buyer_namelastname', 'buyer_phone', 'request_title', 'request_discription')
    ordering = ('-ticket_time',)
    readonly_fields = ('ticket_id', 'ticket_time', 'ip_address', 'user', 'buyer_namelastname', 'buyer_phone')
    autocomplete_fields = ('user',)
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('ticket_id', 'ticket_type', 'request_title', 'request_discription', 'ticket_time')
        }),
        ('اطلاعات فرستنده', {
            'fields': ('user', 'buyer_namelastname', 'buyer_phone', 'ip_address')
        }),
    )


@admin.register(BuyTicket)
class BuyTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'product', 'gain', 'price', 'buy_time')
    search_fields = ('id', 'name', 'phone', 'post_code', 'address', 'product__kind')
    ordering = ('-buy_time',)
    readonly_fields = ('id', 'buy_time', 'ip_address')
    autocomplete_fields = ('product',)
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('id', 'product', 'gain', 'price', 'buy_time')
        }),
        ('اطلاعات خریدار', {
            'fields': ('name', 'phone', 'post_code', 'address')
        }),
        ('اطلاعات سیستم', {
            'fields': ('ip_address',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogCategories)
class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'get_post_count')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    def get_post_count(self, obj):
        return obj.post_count()
    get_post_count.short_description = 'تعداد پست‌ها'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'auther', 'category', 'created_at', 'is_confirmed')
    list_filter = ('category', 'is_confirmed', 'auther')
    search_fields = ('title', 'slug', 'auther__username')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('auther', 'category')
    list_editable = ('is_confirmed',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor},
    }
    fieldsets = (
        ('محتوای اصلی', {
            'fields': ('title', 'slug', 'category', 'auther', 'content_blocks', 'cover_image')
        }),
        ('رسانه‌ها (اختیاری)', {
            'fields': (('image1', 'image2'), ('image3', 'image4'), ('image5', 'image6'), 'image7'),
            'classes': ('collapse',)
        }),
        ('اطلاعات تکمیلی و SEO', {
            'fields': ('tags', 'time_to_read', 'refrence_url', 'refrence_url_text')
        }),
        ('وضعیت انتشار', {
            'fields': ('is_confirmed', 'created_at', 'views')
        }),
    )
    readonly_fields = ('created_at', 'views')


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1
    max_num = 3
    verbose_name_plural = "سوابق کاری (حداکثر ۳ مورد)"


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    max_num = 3
    verbose_name_plural = "سوابق تحصیلی (حداکثر ۳ مورد)"


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone_number')
    search_fields = ('name', 'title')
    inlines = [WorkExperienceInline, EducationInline]
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('slug','is_confirmed','role','name', 'title', 'avatar', 'about_me', 'age', 'email', 'phone_number', 'address')
        }),
        ('فایل‌ها', {
            'fields': ('resume_file',)
        }),
        ('مهارت‌ها', {
            'description': 'مهارت‌ها را به فرمت "نام,درصد" وارد کرده و با ; جدا کنید. (مثال: HTML,95;CSS,40)',
            'fields': ('skills_category_1', 'skills_category_2')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('twitter_url', 'telegram_url', 'instagram_url', 'github_url'),
            'classes': ('collapse',)
        }),
    )
