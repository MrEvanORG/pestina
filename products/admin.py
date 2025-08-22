from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from jsoneditor.forms import JSONEditor
from .addons import send_admin_notif
from .models import (
    SeoData, Product, Ticket, BuyTicket, BlogCategories, 
    BlogPost, Resume, Education, WorkExperience, models, User , 
)

try:
    from products.templatetags.custom_filters import format_weight, format_toman, to_jalali_persian
except ImportError:
    def format_weight(value): return f"{value} kg"
    def format_toman(value): return f"{value} Toman"
    def to_jalali_persian(value): return value

# =============================================================================
# Register Superuser Models
# =============================================================================

@admin.register(SeoData)
class SeoDataAdmin(admin.ModelAdmin):

    list_display = ("path", "title", "meta_description")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone_number", "is_staff", "is_verified")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'province', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined','ip_address')}),
    )
    readonly_fields = ("ip_address",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_verified", "province")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    ordering = ("-date_joined",)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    actions = ['send_custom_sms']

    @admin.action(description='ارسال پیامک سفارشی به کاربران')
    def send_custom_sms(self, request, queryset):
        # ID کاربران انتخاب شده را در سشن ذخیره می‌کنیم
        selected_ids = list(queryset.values_list('id', flat=True))
        request.session['selected_user_ids_for_sms'] = selected_ids
        
        # کاربر را به صفحه فرم ارسال پیامک هدایت می‌کنیم
        return HttpResponseRedirect(reverse('send_sms_page'))
    
@admin.register(Product)
class SuperUserProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'user', 'kind', 'status', 'price', 'inventory', 'is_pestina_product', 'is_confirmed')
    list_filter = ('kind', 'status', 'quality', 'is_confirmed', 'is_pestina_product', 'free_shipping')
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'discription')
    ordering = ('-upload_time',)
    readonly_fields = ('ip_address','views','upload_time')
    autocomplete_fields = ('user',)
    list_editable = ('price', 'inventory', 'is_confirmed')
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('user', 'slug', 'kind', 'status', 'ounce', 'quality', 'photo')}),
        ('قیمت و موجودی', {'fields': ('price', 'inventory', 'show_inventory', 'min_order', 'max_order')}),
        ('اطلاعات ارسال', {'fields': ('free_shipping', 'shipping_cost')}),
        ('وضعیت و توضیحات', {'fields': ('is_confirmed', 'is_pestina_product', 'discription')}),
        ('اطلاعات سیستم', {'fields': ('ip_address', 'upload_time','views'), 'classes': ('collapse',)})
    )

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(BuyTicket)
class SuperUserBuyTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'product', 'gain', 'price', 'buy_time')
    search_fields = ('id', 'name', 'phone', 'post_code', 'address', 'product__kind')
    ordering = ('-buy_time',)
    readonly_fields = ('id', 'buy_time', 'ip_address')
    autocomplete_fields = ('product',)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'ticket_type', 'request_title', 'buyer_namelastname', 'buyer_phone', 'ticket_time')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(BlogCategories)
class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'get_post_count')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    def get_post_count(self, obj):
        return obj.post_count()
    get_post_count.short_description = 'تعداد پست‌ها'

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

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

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


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

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# =============================================================================
# Register Farmer Models on Admin
# =============================================================================

class FarmerAdminSite(admin.AdminSite):
    site_header = 'پنل کاربری پستینا'
    site_title = 'داشبورد'
    index_title = 'به پنل مدیریت خود خوش آمدید'
    # login_template = "l-pages/login.html"

farmer_admin_site = FarmerAdminSite(name='farmer_admin')

@admin.register(User, site=farmer_admin_site)
class FarmerUserAdmin(BaseUserAdmin):

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        model._meta.verbose_name = 'مشخصات من'
        model._meta.verbose_name_plural = 'مشخصات من'

    list_display = ('first_name', 'last_name', 'email', 'jalali_date_joined')
    list_display_links = ('first_name', 'last_name')
    search_fields = ()
    list_filter = ()

    fieldsets = (
        ('اطلاعات کاربری (قابل ویرایش)', {
            'fields': ('first_name', 'last_name', 'email', 'change_password_link')
        }),
        ('اطلاعات تکمیلی (فقط مشاهده)', {
            'fields': ('phone_number', 'province', 'city', 'jalali_date_joined')
        }),
    )
    readonly_fields = ('phone_number', 'province', 'city', 'jalali_date_joined', 'change_password_link')

    def change_password_link(self, obj):
        if obj.pk:
            url = reverse('farmer_admin:auth_user_password_change', args=[obj.pk])
            return format_html('<a class="button" href="{}">تغییر رمز عبور</a>', url)
        return "ابتدا کاربر را ذخیره کنید"
    change_password_link.short_description = 'تغییر رمز عبور'

    def jalali_date_joined(self, obj):
        return to_jalali_persian(obj.date_joined)
    jalali_date_joined.short_description = "تاریخ عضویت"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk=request.user.pk)

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Product, site=farmer_admin_site)
class FarmerProductAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        model._meta.verbose_name = 'محصول'
        model._meta.verbose_name_plural = 'محصولات من'

    list_display = ('kind', 'status', 'price', 'inventory', 'is_confirmed_status', 'jalali_date_upload','views')
    fieldsets = (
        ('مشخصات اصلی محصول', {'fields': ('photo', 'kind', 'status', 'ounce', 'quality', 'discription')}),
        ('قیمت و موجودی', {'fields': ('price', 'inventory', 'show_inventory', 'min_order', 'max_order')}),
        ('جزئیات ارسال', {'fields': ('free_shipping', 'shipping_cost')}),
        ('اطلاعات سیستم',{'fields':('jalali_date_upload','views')}),
    )
    readonly_fields = ('jalali_date_upload','views')

    def jalali_date_upload(self, obj):
        return to_jalali_persian(obj.upload_time)
    jalali_date_upload.short_description = "تاریخ بارگذاری"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change :
            from threading import Thread
            Thread(target=send_admin_notif,kwargs={"mode":"new_product","product":obj}).start()
            from products.addons import get_ip 
            obj.ip_address = get_ip(request)

        if not obj.pk:
            obj.user = request.user
        obj.is_confirmed = False
        super().save_model(request, obj, form, change)
        
    def is_confirmed_status(self, obj):
        if obj.is_confirmed:
            return format_html('<span style="color: green;">● تایید شده</span>')
        return format_html('<span style="color: orange;">● در انتظار بازبینی</span>')
    is_confirmed_status.short_description = "وضعیت تایید"

@admin.register(BuyTicket, site=farmer_admin_site)
class FarmerBuyTicketAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        model._meta.verbose_name_plural = 'درخواست‌های خرید'
        model._meta.verbose_name = 'درخواست خرید'
        
    list_display = ('name', 'phone', 'product', 'formatted_price', 'jalali_buy_time')
    list_display_links = ('name',)
    fieldsets = (
        ('مشخصات خریدار', {'fields': ('name', 'phone')},),
        ('جزئیات سفارش', {'fields': ('product', 'formatted_gain', 'formatted_price')},),
        ('آدرس و کدپستی', {'fields': ('address', 'post_code')},),
        ('اطلاعات سفارش', {'fields': ('jalali_buy_time',)},),
    )

    def formatted_gain(self, obj):
        return format_weight(obj.gain)
    formatted_gain.short_description = "مقدار سفارش"

    def formatted_price(self, obj):
        return format_toman(obj.price)
    formatted_price.short_description = "قیمت نهایی"

    def jalali_buy_time(self, obj):
        return to_jalali_persian(obj.buy_time)
    jalali_buy_time.short_description = "تاریخ سفارش"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(product__user=request.user)

    def get_readonly_fields(self, request, obj=None):

        return [
            'product', 'name', 'phone', 'address', 'post_code', 'message_status', 
            'formatted_gain', 'formatted_price', 'jalali_buy_time'
        ]

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
