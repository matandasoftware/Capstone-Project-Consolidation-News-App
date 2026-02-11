"""
REST API Serializers for the News Application.

This module contains Django REST Framework serializers that convert
model instances to JSON for API responses:
- ArticleSerializer: Serializes Article objects with related data
- PublisherSerializer: Serializes Publisher objects with article counts
- JournalistSerializer: Serializes journalist user data

Serializers handle data validation and nested relationships.
"""
from rest_framework import serializers
from .models import Article, Publisher, CustomUser


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model.
    Converts Article objects to JSON for API responses.
    Similar to StoreSerializer from your module.
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    publisher_name = serializers.ReadOnlyField(source='publisher.name')
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'summary',
            'author',
            'author_username',
            'publisher',
            'publisher_name',
            'is_approved',
            'is_independent',
            'created_at',
            'published_at'
        ]
        read_only_fields = ['slug', 'author', 'is_approved', 'is_independent', 'created_at']  # Added 'author' here


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for Publisher model.
    Returns publisher information with article count.
    """
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'description',
            'website',
            'article_count',
            'created_at'
        ]
    
    def get_article_count(self, obj):
        """Return count of approved articles for this publisher"""
        return obj.articles.filter(is_approved=True).count()


class JournalistSerializer(serializers.ModelSerializer):
    """
    Serializer for Journalist users.
    Only serializes users with JOURNALIST role.
    """
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'article_count',
            'date_joined'
        ]
    
    def get_article_count(self, obj):
        """Return count of approved articles by this journalist"""
        return obj.articles.filter(is_approved=True).count()

