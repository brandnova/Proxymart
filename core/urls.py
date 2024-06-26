from django.urls import path
from .views import index, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('logout/', user_logout, name='user_logout'),
]
