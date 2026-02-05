# Register your models here.
from django.contrib import admin
from .models import Category, Product, Store, Order, OrderItem, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']
    
    # Remove the duplicate "ADD CATEGORY +" button from the changelist page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin configuration for Store model."""
    list_display = ['name', 'vendor', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'vendor__username']
    ordering = ['-created_at']
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Remove the duplicate "ADD PRODUCT +" button from the changelist page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)

    

class OrderItemInline(admin.TabularInline):
    """Inline display of order items within order admin."""
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'get_subtotal']
    can_delete = False
    
    def get_subtotal(self, obj):
        return f"R{obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = ['id', 'buyer', 'total_amount', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['buyer__username', 'buyer__email']
    readonly_fields = ['buyer', 'total_amount', 'order_date']
    list_editable = ['status']
    ordering = ['-order_date']
    inlines = [OrderItemInline]
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ['product', 'user', 'rating', 'verified', 'created_at']
    list_filter = ['verified', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    readonly_fields = ['user', 'product', 'verified', 'created_at']
    ordering = ['-created_at']
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)