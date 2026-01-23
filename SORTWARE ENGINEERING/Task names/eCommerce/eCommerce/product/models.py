from django.db import models
from django.conf import settings

class Store(models.Model):
    """Model representing a vendor's store."""
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stores'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name

class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Model representing a product in the eCommerce store."""
    name = models.CharField(max_length=255)
    store = models.ForeignKey(
     Store,
      on_delete=models.CASCADE,
     related_name='products',
        null=True,
        blank=True
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(
      Category,
     on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=False
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    def get_stock_status(self):
        """Return stock status: 'out', 'low', or 'in'"""
        if self.stock == 0:
            return 'out'
        elif self.stock <= 10:
            return 'low'
        else:
            return 'in'
    
    def get_stock_display(self):
        """Return display text and badge class for stock status"""
        status = self.get_stock_status()
        if status == 'out':
            return {'text': 'Out of Stock', 'class': 'bg-danger', 'show_qty': False}
        elif status == 'low':
            return {'text': f'In Store Only ({self.stock} left)', 'class': 'bg-warning', 'show_qty': True}
        else:
            return {'text': f'In Stock ({self.stock})', 'class': 'bg-success', 'show_qty': True}



class Order(models.Model):
    """Model representing a buyer's order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username}"


class OrderItem(models.Model):
    """Model representing individual items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def get_subtotal(self):
        return self.quantity * self.price



class Review(models.Model):
    """Model representing a product review."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    )
    comment = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-verified', '-created_at']  # Verified first, then newest
        unique_together = ['product', 'user']  # One review per user per product
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        """Automatically set verified status based on purchase history."""
        # Check if user has purchased this product
        has_purchased = OrderItem.objects.filter(
            order__buyer=self.user,
            product=self.product
        ).exists()
        self.verified = has_purchased
        super().save(*args, **kwargs)