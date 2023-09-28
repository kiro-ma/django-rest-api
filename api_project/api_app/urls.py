from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='user-detail'),
    path('api/user_password/<int:pk>/', views.ChangePasswordViewSet.as_view({'put': 'update'}), name='change-password'),

    path('api/user/username/<str:username>/', views.UserViewSet.as_view({'get': 'get_by_username'}), name='user-get-by-username'),

    path('api/item/', views.ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-list'),
    path('api/item/<int:pk>/', views.ItemViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='item-detail'),
    path('api/item/nome/<str:nome_str>', views.ItemViewSet.as_view({'get': 'list_by_nome'}), name='item-nome-retrieve'),

    path('api/pedido/', views.PedidoViewSet.as_view({'get': 'list', 'post': 'create'}), name='pedido-list'),
    path('api/pedido/<int:pk>/', views.PedidoViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='pedido-detail'),
    path('api/pedido/data/', views.PedidoViewSet.as_view({'get': 'list_by_data'}), name='pedido-data-list'),
    path('api/pedido/user/<int:user_id>/', views.PedidoViewSet.as_view({'get': 'list_by_user'}), name='pedido-list-by-user'),
]
