from django.urls import path
from .views import genreate_token,Sign_User_Up,Activate_User,Get_User_info,Log_User_In,Log_User_Out_Unity,User_Login_WebPage,User_SignUp_WebPage,Load_First_Page
from .views import Log_User_Out_WebPage,Search_Users
urlpatterns=[
    path('',Load_First_Page.as_view(),name='Load_First_Page'),
    path('Log_In',User_Login_WebPage.as_view(),name='User_Login_Web'),
path('Log_out',Log_User_Out_WebPage.as_view(),name='User_Logout_Web'),
    path('Search_Users',Search_Users.as_view(),name='Search_For_Users'),
path('Sign_up/',User_SignUp_WebPage.as_view(),name='User_Signup_Webpage'),
    path('get_token',genreate_token.as_view(),name='get_token'),
path('sign_up/',Sign_User_Up.as_view(),name='Sign_User_Up')
             ,path('Activate_user/<str:act_code>',Activate_User,name='Activate_User')
,path('Get_User_Info/',Get_User_info,name='Get_User_info')
,path('Log_User_In',Log_User_In.as_view(),name='Get_User_info')
             ,path('Log_User_Out_Unity/',Log_User_Out_Unity,name='Log_User_Out_Unity')
             ]