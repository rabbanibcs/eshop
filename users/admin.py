from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Wishlist, Cart,Address,Order
from django.conf import settings


class CustomUserAdmin(UserAdmin):
    model = settings.AUTH_USER_MODEL
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name',)
    list_display_links = ("email",)
    search_fields = ('last_name', 'email',)
    ordering = ('last_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)


# register custom user model
admin.site.register(Users, CustomUserAdmin)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
