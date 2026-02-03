from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Store, Product, Category, Review
from .serializers import StoreSerializer, ProductSerializer, CategorySerializer, ReviewSerializer 


@api_view(['GET'])
def view_stores(request):
    """
    GET /api/stores/
    Returns list of all stores.
    Optional filter: ?vendor=1 (stores by specific vendor)
    No authentication required.
    """
    if request.method == "GET":
        stores = Store.objects.all()
        
        # Optional: Filter by vendor
        vendor_id = request.GET.get('vendor')
        if vendor_id:
            stores = stores.filter(vendor_id=vendor_id)
        
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse(data=serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_store(request):
    """
    POST /api/stores/add/
    Creates new store.
    Requires authentication.
    Security: User can only create stores for themselves.
    """
    if request.method == "POST":
        # SECURITY: Check vendor ID matches logged-in user
        if request.user.id == request.data['vendor']:
            serializer = StoreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return JsonResponse(
            {'error': 'ID mismatch: User ID and vendor ID do not match'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def view_products(request):
    """
    GET /api/products/
    Returns list of all active products.
    Optional filters: 
        ?category=1 - Filter by category
        ?store=1 - Filter by store
        ?min_price=10 - Minimum price
    No authentication required.
    """
    if request.method == "GET":
        products = Product.objects.filter(is_active=True)
        
        # Optional: Filter by category
        category_id = request.GET.get('category')
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Optional: Filter by store
        store_id = request.GET.get('store')
        if store_id:
            products = products.filter(store_id=store_id)
        
        # Optional: Filter by min price
        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(price__gte=min_price)
        
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
def view_categories(request):
    """
    GET /api/categories/
    Returns list of all categories.
    No authentication required.
    """
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(data=serializer.data, safe=False)



@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    """
    POST /api/products/add/
    Add product to store.
    Requires authentication.
    Security: User can only add products to their own stores.
    """
    if request.method == "POST":
        # Get the store
        store_id = request.data.get('store')
        if not store_id:
            return JsonResponse(
                {'error': 'Store ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        store = get_object_or_404(Store, pk=store_id)
        
        # SECURITY: Check store belongs to logged-in user
        if store.vendor != request.user:
            return JsonResponse(
                {'error': 'You can only add products to your own stores'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def view_reviews(request):
    """
    GET /api/reviews/
    Get all reviews.
    Optional filter: ?product=1 (reviews for specific product)
    No authentication required.
    """
    if request.method == "GET":
        reviews = Review.objects.all()
        
        # Optional: Filter by product
        product_id = request.GET.get('product')
        if product_id:
            reviews = reviews.filter(product_id=product_id)
        
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(data=serializer.data, safe=False)