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
from . import views as index_view
from django.urls import path
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('', index_view.index, name="index_registration_form"),
    path('login/', index_view.user_login_form, name="index_login_form"),
    path('logout/', index_view.user_logout, name="index_logout"),
    path('export', index_view.user_time_chart_export, name="exportcsv"),
    path('feedback', index_view.submit_feedback, name="feedback"),
    path('changepass', index_view.user_password_change, name="password_change"),
    path('changeemail', index_view.user_email_change, name="email_change"),
    path('password_reset',auth_view.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    # path('password_reset_done',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('password_reset_done',auth_view.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    # path('password_reset/complete',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
    path('password_reset/complete',index_view.user_login_form,name="password_reset_complete"),
]
