from django.urls import path
from .views import loginview,user_profile,user_register,SignUpView,edit_user,logoutview,EditUserView
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeView,PasswordChangeDoneView,\
    PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

from django.contrib.auth import views as auth_views

urlpatterns=[
    path('login/', loginview, name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',user_profile,name='profile'),
    path('password_change/',PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/',PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('signup/',user_register,name='user_register'),
    # path('profile/edit/',edit_user,name='user_edit')
    path('profile/edit/',EditUserView.as_view(),name='user_edit')
    # path('signup/',SignUpView.as_view(),name='user_register')
]