from rest_framework.serializers import ModelSerializer
from .models import Product

class Product_serializer(ModelSerializer):
    class Meta:
        model=Product
        fields=['id','pr_type','price','is_availible','get_thumbnail','product_name']