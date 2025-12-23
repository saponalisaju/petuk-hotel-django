import random
import re
from core.models import Product, Category, Vendor, CartOrder, \
    CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from blog.models import Post
from django.db.models import Min, Max
from django.contrib import messages
from taggit.models import Tag


def parse_price(value):
    """
    Ensure price is numeric. Strip Bangla text or currency symbols if present.
    """
    cleaned = re.sub(r'[^0-9\.]', '', str(value))
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0


def core_context(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    latest_products = Product.objects.filter(product_status='published').order_by('-date')

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except Exception:
        wishlist = None

    all_product_tags = Tag.objects.filter(product__isnull=False).distinct()
    random_product_tags = random.sample(list(all_product_tags), min(6, len(all_product_tags)))

    blog_posts = Post.objects.filter(post_status='published').order_by("-date_created")

    cart_total_amount = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            qty = int(item.get('qty', 0))
            price = parse_price(item.get('price', 0))
            cart_total_amount += qty * price

    return {
        'categories': categories,
        'vendors': vendors,
        'wishlist': wishlist,
        'min_max_price': min_max_price,
        'cart_total_amount': cart_total_amount,
        'latest_products': latest_products,
        'random_product_tags': random_product_tags,
        'blog_posts': blog_posts,
    }
