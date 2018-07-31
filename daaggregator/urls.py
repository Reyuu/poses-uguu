"""daaggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from mainapp import views as mainapp_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poses', mainapp_views.main_view),
    path('', mainapp_views.index),
    path('get_random_pose', mainapp_views.get_random_pose),
    path('report_image', mainapp_views.report_image),
    path('suggest', mainapp_views.suggest),
    path('feedback', mainapp_views.feedback),
    path('login', auth_views.login, name="login"),
    path('logout', mainapp_views.logout_view, name="logout"),
    path('mod_panel', mainapp_views.mod_index),
    path('mod_get_all_reports', mainapp_views.mod_get_all_reports),
    path('mod_handle_report', mainapp_views.mod_handle_report),
    path('mod_get_pic_by_id', mainapp_views.mod_get_pic_by_id),
]
