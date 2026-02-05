from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, Store, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StoreForm, ProductForm, CategoryForm, ReviewForm

def is_vendor(user):
    """Check if user is in Vendors group."""
    return user.groups.filter(name='Vendors').exists()


def product_list(request):
    """View to display a list of all products."""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    selected_category = None
    page_title = "Products"
    
    if category_id:
        products = products.filter(category_id=category_id)
        try:
            selected_category = Category.objects.get(id=category_id)
            page_title = f"Products - {selected_category.name}"
        except Category.DoesNotExist:
            pass
    
    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "page_title": page_title,
    }
    return render(request, "product/product_list.html", context)


def product_detail(request, pk):
    """View to display details of a specific product."""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    context = {
        "product": product,
        "page_title": product.name,
    }
    return render(request, "product/product_detail.html", context)


def category_list(request):
    """View to display a list of all categories."""
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "page_title": "Categories",
    }
    return render(request, "product/category_list.html", context)


def category_detail(request, pk):
    """View to display products in a specific category."""
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, is_active=True)
    context = {
        "category": category,
        "products": products,
        "page_title": category.name,
    }
    return render(request, "product/category_detail.html", context)

# Store Management (Vendors Only)

@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def store_list(request):
    """View vendor's stores."""
    stores = Store.objects.filter(vendor=request.user)
    context = {
        'stores': stores,
        'page_title': 'My Stores',
    }
    return render(request, 'product/store_list.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def store_create(request):
    """Create new store."""
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            messages.success(request, f'Store "{store.name}" created successfully!')
            return redirect('product:store_list')
    else:
        form = StoreForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Store',
        'action': 'Create',
    }
    return render(request, 'product/store_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def store_detail(request, pk):
    """View store details and products."""
    store = get_object_or_404(Store, pk=pk)
    
    # Check ownership
    if store.vendor != request.user:
        messages.error(request, 'You can only view your own stores.')
        return redirect('product:store_list')
    
    products = store.products.filter(is_active=True)
    context = {
        'store': store,
        'products': products,
        'page_title': store.name,
    }
    return render(request, 'product/store_detail.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def store_update(request, pk):
    """Update store."""
    store = get_object_or_404(Store, pk=pk)
    
    # Check ownership
    if store.vendor != request.user:
        messages.error(request, 'You can only edit your own stores.')
        return redirect('product:store_list')
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store = form.save()
            messages.success(request, f'Store "{store.name}" updated successfully!')
            return redirect('product:store_detail', pk=store.pk)
    else:
        form = StoreForm(instance=store)
    
    context = {
        'form': form,
        'store': store,
        'page_title': f'Edit {store.name}',
        'action': 'Update',
    }
    return render(request, 'product/store_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def store_delete(request, pk):
    """Delete store."""
    store = get_object_or_404(Store, pk=pk)
    
    # Check ownership
    if store.vendor != request.user:
        messages.error(request, 'You can only delete your own stores.')
        return redirect('product:store_list')
    
    if request.method == 'POST':
        store_name = store.name
        store.delete()
        messages.success(request, f'Store "{store_name}" deleted successfully!')
        return redirect('product:store_list')
    
    context = {
        'store': store,
        'page_title': f'Delete {store.name}',
    }
    return render(request, 'product/store_confirm_delete.html', context)

# Product Management (Vendors Only)

@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_product_list(request):
    """View vendor's products across all stores."""
    # Get all products from vendor's stores
    vendor_stores = Store.objects.filter(vendor=request.user)
    products = Product.objects.filter(store__in=vendor_stores).order_by('-created_at')
    
    # Check if vendor has stores and categories
    has_stores = vendor_stores.exists()
    has_categories = Category.objects.exists()
    
    context = {
        'products': products,
        'has_stores': has_stores,
        'has_categories': has_categories,
        'page_title': 'My Products',
    }
    return render(request, 'product/vendor_product_list.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_product_create(request, store_pk=None):
    """Create new product."""
    # Check if vendor has any stores
    vendor_stores = Store.objects.filter(vendor=request.user)
    if not vendor_stores.exists():
        messages.warning(request, 'You need to create a store before adding products.')
        return redirect('product:store_create')
    
    # Check if any categories exist
    if not Category.objects.exists():
        messages.warning(request, 'You need to create at least one category before adding products.')
        return redirect('product:vendor_category_create')
    
    # If store_pk provided, pre-select that store
    initial = {}
    if store_pk:
        store = get_object_or_404(Store, pk=store_pk, vendor=request.user)
        initial['store'] = store
    
    if request.method == 'POST':
        form = ProductForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product:store_detail', pk=product.store.pk)
    else:
        form = ProductForm(user=request.user, initial=initial)
    
    context = {
        'form': form,
        'page_title': 'Add New Product',
        'action': 'Create',
    }
    return render(request, 'product/vendor_product_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_product_update(request, pk):
    """Update product."""
    product = get_object_or_404(Product, pk=pk)
    
    # Check ownership (product's store must belong to vendor)
    if product.store.vendor != request.user:
        messages.error(request, 'You can only edit your own products.')
        return redirect('product:vendor_product_list')
    
    if request.method == 'POST':
        form = ProductForm(user=request.user, data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product:store_detail', pk=product.store.pk)
    else:
        form = ProductForm(user=request.user, instance=product)
    
    context = {
        'form': form,
        'product': product,
        'page_title': f'Edit {product.name}',
        'action': 'Update',
    }
    return render(request, 'product/vendor_product_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_product_delete(request, pk):
    """Delete product."""
    product = get_object_or_404(Product, pk=pk)
    
    # Check ownership
    if product.store.vendor != request.user:
        messages.error(request, 'You can only delete your own products.')
        return redirect('product:vendor_product_list')
    
    if request.method == 'POST':
        store_pk = product.store.pk
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('product:store_detail', pk=store_pk)
    
    context = {
        'product': product,
        'page_title': f'Delete {product.name}',
    }
    return render(request, 'product/vendor_product_confirm_delete.html', context)



# Shopping Cart Helper Functions

def get_cart(request):
    """Get cart from session or create empty cart."""
    cart = request.session.get('cart', {})
    return cart


def add_to_cart_session(request, product_id, quantity=1):
    """Add product to cart session."""
    cart = get_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def update_cart_session(request, product_id, quantity):
    """Update product quantity in cart."""
    cart = get_cart(request)
    product_id_str = str(product_id)
    
    if quantity > 0:
        cart[product_id_str] = quantity
    else:
        cart.pop(product_id_str, None)
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def remove_from_cart_session(request, product_id):
    """Remove product from cart."""
    cart = get_cart(request)
    product_id_str = str(product_id)
    cart.pop(product_id_str, None)
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def get_cart_items(request):
    """Get cart items with product details and calculate totals."""
    cart = get_cart(request)
    items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            subtotal = product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            # Remove invalid products from cart
            cart.pop(product_id, None)
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return {
        'items': items,
        'total': total,
        'count': sum(cart.values())
    }


def clear_cart(request):
    """Clear all items from cart."""
    request.session['cart'] = {}
    request.session.modified = True

# Email Functions

def send_invoice_email(order):
    """Send invoice email to buyer after checkout."""
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    
    # Build email subject
    subject = f'Order Confirmation #{order.id} - eCommerce Store'
    
    # Build email body (HTML)
    html_message = render_to_string('product/email_invoice.html', {
        'order': order,
        'buyer': order.buyer,
    })
    
    # Create email
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email='noreply@ecommerce.com',
        to=[order.buyer.email],
    )
    email.content_subtype = 'html'  # Send as HTML
    
    # Send email
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Shopping Cart Views (Buyers Only)

@login_required
def add_to_cart(request, pk):
    """Add product to cart."""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    cart = get_cart(request)
    current_quantity = cart.get(str(pk), 0)
    
    if current_quantity >= product.stock:
        messages.warning(request, f'Sorry, only {product.stock} units of {product.name} available.')
        return redirect('product:product_detail', pk=pk)
    
    add_to_cart_session(request, pk, 1)
    messages.success(request, f'{product.name} added to cart!')
    
    next_url = request.GET.get('next', 'product:product_list')
    return redirect(next_url)


@login_required
def view_cart(request):
    """View shopping cart."""
    cart_data = get_cart_items(request)
    
    context = {
        'cart_items': cart_data['items'],
        'cart_total': cart_data['total'],
        'cart_count': cart_data['count'],
        'page_title': 'Shopping Cart',
    }
    return render(request, 'product/cart.html', context)


@login_required
def update_cart(request, pk):
    """Update product quantity in cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, pk=pk)
        
        if quantity > product.stock:
            messages.warning(request, f'Sorry, only {product.stock} units available.')
            quantity = product.stock
        
        update_cart_session(request, pk, quantity)
        messages.success(request, 'Cart updated!')
    
    return redirect('product:view_cart')


@login_required
def remove_from_cart(request, pk):
    """Remove product from cart."""
    product = get_object_or_404(Product, pk=pk)
    remove_from_cart_session(request, pk)
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('product:view_cart')


@login_required
def checkout(request):
    """Process checkout and create order."""
    cart_data = get_cart_items(request)
    
    if not cart_data['items']:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product:product_list')
    
    if request.method == 'POST':
        order = Order.objects.create(
            buyer=request.user,
            total_amount=cart_data['total'],
            status='pending'
        )
        
        for item in cart_data['items']:
            product = item['product']
            quantity = item['quantity']
            
            if quantity > product.stock:
                order.delete()
                messages.error(request, f'Insufficient stock for {product.name}. Please update your cart.')
                return redirect('product:view_cart')
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            product.stock -= quantity
            product.save()
        
        clear_cart(request)
        
        # Send invoice email
        email_sent = send_invoice_email(order)
        
        if email_sent:
            messages.success(request, f'Order #{order.id} placed successfully! Invoice sent to {order.buyer.email}')
        else:
            messages.warning(request, f'Order #{order.id} placed successfully! (Email could not be sent)')
        
        return redirect('product:order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_data['items'],
        'cart_total': cart_data['total'],
        'cart_count': cart_data['count'],
        'page_title': 'Checkout',
    }
    return render(request, 'product/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Show order confirmation page."""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    context = {
        'order': order,
        'page_title': f'Order #{order.id} Confirmation',
    }
    return render(request, 'product/order_confirmation.html', context)


@login_required
def my_orders(request):
    """View buyer's order history."""
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items__product')
    
    context = {
        'orders': orders,
        'page_title': 'My Orders',
    }
    return render(request, 'product/my_orders.html', context)



# Review System (Buyers Only)

@login_required
def add_review(request, pk):
    """Add or update review for a product."""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    # Check if user is a buyer
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can leave reviews.')
        return redirect('product:product_detail', pk=pk)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()  # This automatically sets verified status
            
            if existing_review:
                messages.success(request, 'Your review has been updated!')
            else:
                messages.success(request, 'Thank you for your review!')
            
            return redirect('product:product_detail', pk=pk)
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'product': product,
        'existing_review': existing_review,
        'page_title': f'Review: {product.name}',
    }
    return render(request, 'product/add_review.html', context)


@login_required
def delete_review(request, pk):
    """Delete user's own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    product_pk = review.product.pk
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('product:product_detail', pk=product_pk)
    
    context = {
        'review': review,
        'page_title': 'Delete Review',
    }
    return render(request, 'product/delete_review_confirm.html', context)


# Category Management (Vendors Only)

@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_category_list(request):
    """View all categories (for vendors)."""
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
        'page_title': 'Manage Categories',
    }
    return render(request, 'product/vendor_category_list.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_category_create(request):
    """Create new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('product:vendor_category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Category',
        'action': 'Create',
    }
    return render(request, 'product/vendor_category_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_category_update(request, pk):
    """Update category."""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('product:vendor_category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'page_title': f'Edit {category.name}',
        'action': 'Update',
    }
    return render(request, 'product/vendor_category_form.html', context)


@login_required
@user_passes_test(is_vendor, login_url='/accounts/login/')
def vendor_category_delete(request, pk):
    """Delete category."""
    category = get_object_or_404(Category, pk=pk)
    
    # Check if category has products
    if category.products.exists():
        messages.error(request, f'Cannot delete category "{category.name}" because it has products. Please reassign or delete the products first.')
        return redirect('product:vendor_category_list')
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('product:vendor_category_list')
    
    context = {
        'category': category,
        'page_title': f'Delete {category.name}',
    }
    return render(request, 'product/vendor_category_confirm_delete.html', context)
