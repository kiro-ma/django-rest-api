from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='user-detail'),
    path('api/user_password/<int:pk>/', views.ChangePasswordViewSet.as_view({'put': 'update'}), name='change-password'),

    path('api/item/', views.ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/item/<int:pk>/', views.ItemViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
]
