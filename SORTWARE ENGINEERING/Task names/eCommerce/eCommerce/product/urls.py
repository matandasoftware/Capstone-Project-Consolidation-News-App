from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # Product URLs (Public - Buyers)
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Category URLs (Public)
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    
    # Store URLs (Vendor Only)
    path('stores/', views.store_list, name='store_list'),
    path('store/new/', views.store_create, name='store_create'),
    path('store/<int:pk>/', views.store_detail, name='store_detail'),
    path('store/<int:pk>/edit/', views.store_update, name='store_update'),
    path('store/<int:pk>/delete/', views.store_delete, name='store_delete'),
    
    # Vendor Product Management URLs
    path('vendor/products/', views.vendor_product_list, name='vendor_product_list'),
    path('vendor/product/new/', views.vendor_product_create, name='vendor_product_create'),
    path('vendor/product/new/<int:store_pk>/', views.vendor_product_create, name='vendor_product_create_in_store'),
    path('vendor/product/<int:pk>/edit/', views.vendor_product_update, name='vendor_product_update'),
    path('vendor/product/<int:pk>/delete/', views.vendor_product_delete, name='vendor_product_delete'),
    
    # Vendor Category Management URLs
    path('vendor/categories/', views.vendor_category_list, name='vendor_category_list'),
    path('vendor/category/new/', views.vendor_category_create, name='vendor_category_create'),
    path('vendor/category/<int:pk>/edit/', views.vendor_category_update, name='vendor_category_update'),
    path('vendor/category/<int:pk>/delete/', views.vendor_category_delete, name='vendor_category_delete'),
    
    
    # Shopping Cart URLs (Buyers Only)
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Review URLs (Buyers Only)
    path('product/<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]