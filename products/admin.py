from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from jsoneditor.forms import JSONEditor
from .models import *


@admin.register(User)
class UserAdmin(BaseAdmin):
    model = User
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "is_verified",
        "ip_address",
        "register_time",)
    
    readonly_fields = ("ip_address","register_time")
    list_display_links = ("first_name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "kind",
        "status",
        "ounce",
        "quality",
        "price",
        "show_inventory",
        "inventory",
        "min_order",
        "max_order",
        "free_shipping",
        "shipping_cost",
        "is_pestina_product",
        "is_confirmed",
        "ip_address",
        "upload_time",)
    readonly_fields = ("ip_address","upload_time")
        
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
                    "user",
                    "ticket_id",
                    "buyer_namelastname",
                    "buyer_phone",
                    "ticket_type",
                    "request_title",
                    "request_discription",
                    "ticket_time",
                    "ip_address",)
    readonly_fields = ("ticket_id","ticket_time","ip_address")

@admin.register(BuyTicket)
class BuyTicketAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "name",
                    "phone",
                    "product",
                    "gain",
                    "price",
                    "post_code",
                    "address",
                    "buy_time",
                    "ip_address")
    readonly_fields = ("id","buy_time","ip_address")


@admin.register(BlogCategories)
class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "discription",
        "slug",
        "photo",
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title",
    "slug",
    "auther",
    "category",
    "created_at",
    "cover_image",
    "image1",
    "image1",
    "image3",
    "image4",
    "image5",
    "image6",
    "image7")
    # prepopulated_fields = {'slug':('title',)}
    formfield_overrides = {
        models.JSONField : {'widget':JSONEditor},
    }


# کلاس Inline برای افزودن سوابق کاری در صفحه رزومه
class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1  # همیشه یک فرم خالی برای اضافه کردن نمایش بده
    max_num = 3 # محدودیت برای اضافه کردن حداکثر ۳ مورد
    verbose_name_plural = "سوابق کاری (حداکثر ۳ مورد)"


# کلاس Inline برای افزودن سوابق تحصیلی در صفحه رزومه
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # همیشه یک فرم خالی برای اضافه کردن نمایش بده
    max_num = 3 # محدودیت برای اضافه کردن حداکثر ۳ مورد
    verbose_name_plural = "سوابق تحصیلی (حداکثر ۳ مورد)"


# ثبت نهایی مدل رزومه در پنل ادمین
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone_number')
    search_fields = ('name', 'title')
    inlines = [WorkExperienceInline, EducationInline]

    # دسته‌بندی فیلدها برای نمایش بهتر در پنل ادمین
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
            'classes': ('collapse',) # این بخش به صورت پیش‌فرض بسته باشد
        }),
    )

# EehsaNn8404
