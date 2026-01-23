from django import template

register = template.Library()

@register.filter
def cart_total_quantity(cart):
    """Calculate total quantity of all items in cart."""
    if not cart:
        return 0
    return sum(cart.values())
