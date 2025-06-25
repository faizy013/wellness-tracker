"""
URL configuration for wellness_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from tracker import views as tracker_views
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('signup/', tracker_views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('login/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', tracker_views.dashboard_view, name='dashboard'),
    path('add-water/', tracker_views.add_water_log, name='add_water'),
    path('add-exercise/', tracker_views.add_exercise_log, name='add_exercise'),
    path('add-sleep/', tracker_views.add_sleep_log, name='add_sleep'),
    path('add-mood/', tracker_views.add_mood_log, name='add_mood'),
    path('logs/', tracker_views.view_logs, name='view_logs'),
    path('login/', LogoutView.as_view(next_page='login'), name='logout'),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]
