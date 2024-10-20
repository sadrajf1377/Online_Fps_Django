from django.urls import path, re_path

from .views import Show_All_Posts,Write_A_Comment,Add_Or_Remove_Like,Delete_Comment,View_Posts_By_Hashtag,Post_Details,Create_Post,Show_My_Posts\
    ,Request_Post_Details,Load_Post_Comments


urlpatterns=[
    re_path(r'^show_posts/(?P<group>\w+)?$',Show_All_Posts.as_view(),name='show_all_posts')
             ,path('write_a_comment',Write_A_Comment.as_view(),name='write_a_comment')
,path('add_or_remove_like',Add_Or_Remove_Like.as_view(),name='add_remove_like')
             ,path('delete_comment',Delete_Comment.as_view(),name='delete_comment')
,path('view_posts_by_hashtags/?tag=<str:hash_tag>',View_Posts_By_Hashtag.as_view(),name='view_posts_by_hashtags'),
    path('post_details/<title>',Post_Details.as_view(),name='view_post_details'),
    path('create_post',Create_Post.as_view(),name='create_post')
    ,  path('show_my_posts',Show_My_Posts.as_view(),name='show_my_posts')
,  path('request_post_details',Request_Post_Details.as_view(),name='request_post_details')
,  path('load_comments',Load_Post_Comments.as_view(),name='request_post_comments')
             ]