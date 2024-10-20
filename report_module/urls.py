from django.urls import path

from .views import Fill_Report,Show_My_Reports,Report_Session_Details,Delete_Report,Crete_New_Session,Delete_Session
urlpatterns=[
path('fill_report',Fill_Report.as_view(),name='fill_report'),
path('my_reports',Show_My_Reports.as_view(),name='show_my_reports'),
path('show_session_details/<title>',Report_Session_Details.as_view(),name='show_session_details')
    ,path('delete_report',Delete_Report.as_view(),name='delete_report'),
    path('create_new_session',Crete_New_Session.as_view(),name='create_new_session'),
    path('delete_session', Delete_Session.as_view(), name='delete_session')
]