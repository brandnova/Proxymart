from django.urls import path
from .views import register, login, home, profile, user_info_update, user_logout

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', profile, name='profile'),
    path('user-info/', user_info_update, name='info_update'),
]
