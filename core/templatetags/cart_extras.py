from django import template

register = template.Library()

@register.filter
def multiply(qty, price):
    try:
        return float(qty) * float(price)
    except (ValueError, TypeError):
        return 0
