from django.contrib import admin
from .models import News,News_Comments,comment_like_list,comment_dislike_list
# Register your models here.
admin.site.register(News)
admin.site.register(News_Comments)
admin.site.register(comment_like_list)
admin.site.register(comment_dislike_list)