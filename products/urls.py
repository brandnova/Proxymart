from django.urls import path
# from .views import product_list, add_to_cart, product_detail
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('logout/', views.user_logout, name='user_logout'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    
]
