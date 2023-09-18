from django.contrib import admin
from .models import Category,News,Contact,Comment
# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','status','category','id']
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

class AdminComment(admin.ModelAdmin):
    list_display = ['user']
    actions = ['disable_comment','activate_comments']
    def disable_comment(self,request,queryset):
        queryset.update(active=False)
    def activate_comments(self,request,queryset):
        queryset.update(active=True)

admin.site.register(Comment , AdminComment)