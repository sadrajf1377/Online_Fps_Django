from django.contrib import admin
from .models import User_Bought_Products,Product,Product_List_Detail,Product_Image,Product_Comment
# Register your models here.
admin.site.register(User_Bought_Products)
admin.site.register(Product)
admin.site.register(Product_List_Detail)
admin.site.register(Product_Image)
admin.site.register(Product_Comment)