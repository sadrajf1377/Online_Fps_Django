from django.core.exceptions import ValidationError
from django.db import models
from user_moudle.models import custom_user
# Create your models here.
class Product(models.Model):
    product_types=(('gun_skin','gun_skin'),('character','character'),('gun','gun'),('outfit','outfit'))
    pr_type=models.CharField(max_length=15,choices=product_types,default='gun_skin',null=False,blank=False,verbose_name='product type')
    price=models.DecimalField(verbose_name='price of product',default=0000,max_digits=8,decimal_places=4)
    is_availible=models.BooleanField(default=True,verbose_name='product_availblity')
    creation_date=models.DateTimeField(null=True,auto_now_add=True,verbose_name='date of creation')
    product_name=models.CharField(max_length=100,verbose_name='name of the product',null=False,blank=False,default='')
    multiple = models.BooleanField(default=True,
                                   verbose_name='is user allowed to have multiple instances of this product?')
    description=models.TextField(max_length=1000,verbose_name='product description',null=False,blank=False,default='')
    def get_thumbnail(self):
        try:
            url=self.product_image_set.all()[0].image.url
        except:
           url=''
        return url

class User_Bought_Products(models.Model):
    owner=models.OneToOneField(custom_user,verbose_name='owner of this list',null=False,blank=False,on_delete=models.CASCADE)

class Product_List_Detail(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,verbose_name='product')
    count=models.IntegerField(default=0,verbose_name='how many')

    parent_list=models.ForeignKey(User_Bought_Products,on_delete=models.CASCADE,verbose_name='parent list of details',null=False,blank=False)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.count >1 and not self.product.multiple:
            raise ValueError('cant have multiple of this product')
        else:
            super().save()



class Product_Image(models.Model):
    image=models.ImageField(upload_to='product_images',null=False,blank=False,verbose_name='image file')
    parent_product=models.ForeignKey(Product,null=False,blank=False,on_delete=models.CASCADE,verbose_name='parent product')



class Product_Comment(models.Model):
    parent_comment=models.ForeignKey('Product_Comment',on_delete=models.CASCADE,null=True,blank=True,verbose_name='parent comment')
    comment=models.TextField(max_length=200,verbose_name='comments text',null=False,blank=False)
    creation_date=models.DateTimeField(null=False,blank=False,auto_now_add=True)
    wrote_by=models.ForeignKey(custom_user,on_delete=models.CASCADE,null=False,blank=False,verbose_name='who wrote this comment')
    parent_product=models.ForeignKey(Product,verbose_name='parent product',null=False,blank=False,on_delete=models.CASCADE)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.parent_product.id != self.parent_comment.parent_product.id:
            raise ValidationError('reply and parent must have the same parent product')
        elif self.parent_comment.parent_comment != None:
            raise ValidationError('cannot reply to a reply')
        super().save()
