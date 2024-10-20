from django.urls import path
from .views import Show_Products,Confirm_Order,Show_Products_Web,Get_My_Products_Web,Show_Product_Details,Comment_On_Product,Delete_Comment
urlpatterns=[
    path('/show_products/<start_number>',Show_Products,name='show_products')
    ,path('/show_products_web/',Show_Products_Web.as_view(),name='show_products_web')
  , path('/confirm_order',Confirm_Order.as_view(),name='confirm_order')
    , path('/My_Products', Get_My_Products_Web.as_view(), name='My_Products')
, path('/Product_Details/<str:product_name>', Show_Product_Details.as_view(), name='product_details')
, path('/comment_on_product', Comment_On_Product.as_view(), name='comment_on_product')
, path('/delete_comment', Delete_Comment.as_view(), name='delete_comment')
]