# accounts/urls.py
from django.urls import path
from .views import register_or_login, profile, create_ad, edit_ad, delete_ad, home, logout_view, signup, login_view, profile, my_ads

urlpatterns = [
    path('', home, name='home'),
    
    path('register/', register_or_login, name='register'),
    path('profile/', profile, name='profile'),  # Налаштування профілю
    path('ads/create/', create_ad, name='create_ad'),  # Створення оголошення
    path('ads/<int:id>/edit/', edit_ad, name='edit_ad'),  # Редагування оголошення
    path('ads/<int:id>/delete/', delete_ad, name='delete_ad'),  # Видалення оголошення
    path('ads/my/', my_ads, name='my_ads'),
    path('profile/settings/', profile, name='profile_settings'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
]


