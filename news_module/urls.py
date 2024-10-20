from django.urls import path

from .views import Show_News_Details,Comment_On_News,Like_or_Dislike_Comment,Remove_Comment
urlpatterns=[path('news_detail/<str:title>',Show_News_Details.as_view(),name='show_news_details')
             ,path('comment',Comment_On_News.as_view(),name='comment_on_news')
             ,path('/like_or_dislike_comment',Like_or_Dislike_Comment.as_view(),name='like_or_dislike_comment')
    , path('/remove_comment', Remove_Comment.as_view(), name='remove_comment')
             ]