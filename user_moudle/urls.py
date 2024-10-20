from django.urls import path, re_path
from .views import Update_User_Settings,Update_Profile,Get_Block_list,Unblock_User,Show_User_Profile,Send_Friend_Request,Accept_Friend_Request,Block_User
from .views import Remove_Friend,Show_User_Messages,Submit_Report
from user_moudle.views import Password_Reset
urlpatterns=[
path('settings',Update_User_Settings.as_view(),name='update_user_settings')
,path('profile',Update_Profile.as_view(),name='update_user_profile')
    ,path('',Get_Block_list.as_view(),name='get_block_list')
    , path('unblock_user', Unblock_User.as_view(), name='unblock_user')
    , path('/user_profile/<username>/<to_do>/', Show_User_Profile.as_view(), name='show_user_profile')
, path('send_friend_request/<str:username>', Send_Friend_Request.as_view(), name='send_friend_request')
, path('/accept_friend_request', Accept_Friend_Request.as_view(), name='accept_friend_request')
, path('/block_user', Block_User.as_view(), name='block_user'),
 path('/show_messages', Show_User_Messages.as_view(), name='show_my_messages')
# , path('/send_new_message', Send_New_Message.as_view(), name='send_new_message')
, path('/remove_friend', Remove_Friend.as_view(), name='remove_friend')
, path('/submite_report', Submit_Report.as_view(), name='submit_report')
, path('/ask_for_pass_reset', Password_Reset.Ask_For_Password_Reset.as_view(), name='ask_for_pass_reset')
, path('/pass_reset', Password_Reset.Reset_Password.as_view(), name='pass_reset')
]