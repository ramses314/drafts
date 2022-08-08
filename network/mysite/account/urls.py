from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'account'

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),

    path('pass_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('pass_change/done/', auth_views.PasswordChangeDoneView.as_view(), name = 'password_change_done'),

    path('pass_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('pass_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),

    # ajax
    path('users/follow/', user_follow, name='user_follow'),

    path('user/<username>/<lol>/', user_detail2, name='user_detail2'),
    path('users/', user_list, name='user_list'),

    path('users/<username>/', user_detail, name='user_detail'),




]

