from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Items)

#
# @admin.register(SubCategory)
# class ItemsAdmin(admin.ModelAdmin):
#     pass
#
#
