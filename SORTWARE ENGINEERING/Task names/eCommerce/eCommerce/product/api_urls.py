from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    # Store endpoints
    path('stores/', api_views.view_stores, name='stores'),
    path('stores/add/', api_views.add_store, name='add_store'),
    
    # Product endpoints
    path('products/', api_views.view_products, name='products'),
    path('products/add/', api_views.add_product, name='add_product'),
    
    # Category endpoints
    path('categories/', api_views.view_categories, name='categories'),
    
    # Review endpoints
    path('reviews/', api_views.view_reviews, name='reviews'),
]