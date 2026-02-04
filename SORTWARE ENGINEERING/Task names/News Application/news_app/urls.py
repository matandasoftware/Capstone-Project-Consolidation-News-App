from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Reader views
    path('reader/dashboard/', views.reader_dashboard, name='reader_dashboard'),
    path('reader/publishers/', views.browse_publishers, name='browse_publishers'),
    path('reader/journalists/', views.browse_journalists, name='browse_journalists'),
    path('reader/subscribe/publisher/<int:pk>/', views.subscribe_publisher, name='subscribe_publisher'),
    path('reader/unsubscribe/publisher/<int:pk>/', views.unsubscribe_publisher, name='unsubscribe_publisher'),
    path('reader/subscribe/journalist/<int:pk>/', views.subscribe_journalist, name='subscribe_journalist'),
    path('reader/unsubscribe/journalist/<int:pk>/', views.unsubscribe_journalist, name='unsubscribe_journalist'),
    
    # Journalist views
    path('journalist/dashboard/', views.journalist_dashboard, name='journalist_dashboard'),
    path('journalist/article/new/', views.article_create, name='article_create'),
    path('journalist/article/<int:pk>/edit/', views.article_update, name='article_update'),
    path('journalist/article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('journalist/newsletter/new/', views.newsletter_create, name='newsletter_create'),
    path('journalist/newsletter/<int:pk>/edit/', views.newsletter_update, name='newsletter_update'),
    path('journalist/newsletter/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
    
    # Editor views
    path('editor/dashboard/', views.editor_dashboard, name='editor_dashboard'),
    path('editor/article/<int:pk>/approve/', views.article_approve, name='article_approve'),
    
    # Publisher management
    path('publisher/new/', views.publisher_create, name='publisher_create'),
    
    # API ENDPOINTS (REST API)
    
    # Authentication endpoint
    path('api/login/', api_views.api_login, name='api_login'),
    
    # Public API endpoints (No authentication required)
    path('api/articles/', api_views.view_articles, name='api_articles'),
    path('api/articles/<int:pk>/', api_views.view_article_detail, name='api_article_detail'),
    path('api/publishers/', api_views.view_publishers, name='api_publishers'),
    path('api/journalists/', api_views.view_journalists, name='api_journalists'),
    
    # Protected API endpoints (Authentication required)
    path('api/subscribe/publisher/<int:pk>/', api_views.subscribe_to_publisher, name='api_subscribe_publisher'),
    path('api/subscribe/journalist/<int:pk>/', api_views.subscribe_to_journalist, name='api_subscribe_journalist'),
    path('api/articles/create/', api_views.create_article, name='api_create_article'),
]