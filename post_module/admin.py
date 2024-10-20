from django.contrib import admin
from .models import Post_Model,Post_Images,Post_Comment,Post_Like_List,Hash_Tag

admin.site.register(Post_Model)
admin.site.register(Post_Images)
admin.site.register(Post_Comment)
admin.site.register(Post_Like_List)
admin.site.register(Hash_Tag)
# Register your models here.
