"""
URL configuration for Online_Game_Server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static

from django.urls import path, include

from Online_Game_Server import settings

urlpatterns = [
     path('admin/', admin.site.urls),
     path('',include('auth_module.urls')),
    path('user_module',include('user_moudle.urls'))
    ,path('news',include('news_module.urls')),
    path('messages',include('messages_module.urls'))
    ,path('product_module',include('product_module.urls'))
    ,path('report_module',include('report_module.urls'))
    ,path('post_module',include('post_module.urls'))
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)