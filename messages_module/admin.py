from django.contrib import admin

# Register your models here.
from .models import Post_Forwards,Message_Seen_List
admin.site.register(Post_Forwards)
admin.site.register(Message_Seen_List)
