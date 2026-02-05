from rest_framework import serializers
from .models import Store, Product, Category, Review


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'vendor', 'name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'store', 'store_name', 
                  'image', 'is_active', 'created_at']
        read_only_fields = ['created_at']



class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'user', 'user_username', 
                  'rating', 'comment', 'verified', 'created_at']
        read_only_fields = ['user', 'verified', 'created_at']
