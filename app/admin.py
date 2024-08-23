
from django.contrib import admin
from app.models import Category, Image, Group, Product, Comment, Attribute, Attribute_Key, Attribute_Value
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Image)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'rating' ]


admin.site.register(Attribute_Key)
admin.site.register(Attribute_Value)
admin.site.register(Attribute)
