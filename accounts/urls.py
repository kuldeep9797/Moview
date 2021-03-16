from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('login_process', views.login_process, name='login_process'),
    path('register_process', views.register_process, name='register_process'),
    path('logout_process', views.logout_process, name='logout_process'),
    path('profile_setup', views.profile_setup, name='profile_setup'),
    path('profile_setup_process', views.profile_setup_process, name='profile_setup_process'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('<int:user_id>', views.user_profile, name='user_profile'),
]