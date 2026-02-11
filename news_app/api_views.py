from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Article, Publisher, CustomUser
from .serializers import ArticleSerializer, PublisherSerializer, JournalistSerializer


@api_view(['POST'])
def api_login(request):
    """
    POST /api/login/
    Accepts username and password, returns authentication token.
    Body: {"username": "chris", "password": "password123"}
    Returns: {"token": "abc123xyz", "user_id": 5, "username": "chris", "role": "JOURNALIST"}
    """
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validate credentials
        user = authenticate(username=username, password=password)
        
        if user:
            # Get or create token for this user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


@api_view(['GET'])
def view_articles(request):
    """
    GET /api/articles/
    Returns list of all approved articles.
    No authentication required.
    """
    if request.method == "GET":
        articles = Article.objects.filter(is_approved=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_article_detail(request, pk):
    """
    GET /api/articles/{id}/
    Returns single article by ID.
    No authentication required.
    """
    if request.method == "GET":
        article = get_object_or_404(Article, pk=pk, is_approved=True)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['GET'])
def view_publishers(request):
    """
    GET /api/publishers/
    Returns list of all publishers.
    No authentication required.
    """
    if request.method == "GET":
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def view_journalists(request):
    """
    GET /api/journalists/
    Returns list of all journalists.
    No authentication required.
    """
    if request.method == "GET":
        journalists = CustomUser.objects.filter(role='JOURNALIST')
        serializer = JournalistSerializer(journalists, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribe_to_publisher(request, pk):
    """
    POST /api/subscribe/publisher/{id}/
    Subscribes authenticated user to a publisher.
    Requires authentication.
    """
    if request.method == "POST":
        # Check if user is a READER
        if request.user.role != 'READER':
            return Response(
                {'error': 'Only readers can subscribe to publishers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get publisher
        publisher = get_object_or_404(Publisher, pk=pk)
        
        # Add subscription
        request.user.subscribed_publishers.add(publisher)
        
        return Response(
            {'message': f'Successfully subscribed to {publisher.name}'},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribe_to_journalist(request, pk):
    """
    POST /api/subscribe/journalist/{id}/
    Subscribes authenticated user to a journalist.
    Requires authentication.
    """
    if request.method == "POST":
        # Check if user is a READER
        if request.user.role != 'READER':
            return Response(
                {'error': 'Only readers can subscribe to journalists'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get journalist
        journalist = get_object_or_404(CustomUser, pk=pk, role='JOURNALIST')
        
        # Add subscription
        request.user.subscribed_journalists.add(journalist)
        
        return Response(
            {'message': f'Successfully subscribed to {journalist.username}'},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_article(request):
    """
    POST /api/articles/create/
    Creates new article.
    Requires authentication and JOURNALIST role.
    """
    if request.method == "POST":
        # Check if user is a JOURNALIST
        if request.user.role != 'JOURNALIST':
            return Response(
                {'error': 'Only journalists can create articles'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate and save
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # Set author to current user
            serializer.save(author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
