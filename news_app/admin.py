from django.contrib import admin
from .models import Category,News,Contact
# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','status','category']
    list_filter =['publish_time','status','create_time']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title','body']
    ordering = ['status','publish_time']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display =['name','message','email']