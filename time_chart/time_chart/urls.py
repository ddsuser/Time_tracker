"""time_chart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path , include
from time_chart_all_functionalities import views as func_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('time_chart_index_page.urls')),
    path('', include('time_chart_index_page.urls')),
    path('dashboard', func_view.dashboard , name='dashboard'),
    path('account', func_view.account , name='account'),
    path('start', func_view.user_start_tracking , name='user_start_track'),
    path('stop', func_view.user_stop_track , name='user_stop_track'),
    path('entry', func_view.entry , name='entry'),
    path('delete_user', func_view.user_delete , name='delete_user'),
    path('listview', func_view.listview , name='listview'),
    path('settings', func_view.user_settings1, name='settings'),
]
