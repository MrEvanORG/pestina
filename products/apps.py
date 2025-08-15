from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_farmer_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    FARMER_GROUP_NAME = 'کشاورزان'

    permissions_codenames = [
        'change_user', 'view_user',
        'add_product', 'change_product', 'delete_product', 'view_product',
        'view_buyticket',
    ]

    group, created = Group.objects.get_or_create(name=FARMER_GROUP_NAME)

    if created:
        print(f"گروه '{FARMER_GROUP_NAME}' با موفقیت ایجاد شد. در حال تخصیص دسترسی‌ها...")

        permissions = Permission.objects.filter(codename__in=permissions_codenames)

        group.permissions.set(permissions)
        print("دسترسی‌های لازم به گروه کشاورزان اختصاص داده شد.")

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = "مدیریت اصلی"

    def ready(self):
        post_migrate.connect(create_farmer_group, sender=self)