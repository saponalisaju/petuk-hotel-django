from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Avg, F, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt


# sslcommerz payment gateaway
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.shortcuts import redirect

from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, \
ProductImages, ProductReview, Wishlist, Address, ContactUs
from core.forms import ProductReviewFrom
from taggit.models import Tag
import cloudinary.uploader

def index(request):
	products = Product.objects.filter(product_status='published', featured=True)

	special_offers = Product.objects.filter(product_status='published').annotate(
		discount_percentage=ExpressionWrapper(
			((F('old_price') - F('price')) / F('old_price')) * 100,
			output_field=DecimalField()
		)
    ).order_by('-discount_percentage')[:9]
    
	oldest_products = Product.objects.filter(product_status='published').order_by('date')

	context = {
		"products": products,
		"special_offers": special_offers,
		"oldest_products": oldest_products,
	}
	return render(request, 'core/index.html', context)

def products_list_view(request):
	products = Product.objects.filter(product_status='published')
	context = {
		"products": products
	}
	return render(request, 'core/product-list.html', context)

def category_list_view(request):
	categories = Category.objects.all()
	context = {
		"categories": categories,
	}
	return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
	category = Category.objects.get(cid=cid)
	products = Product.objects.filter(product_status='published', category=category)
	context = {
		"category": category,
		"products": products,
	}
	return render(request, 'core/category-products-list.html', context)

def category_delete_item(request, cid):
    category = get_object_or_404(Category, cid=cid)

    if category.image:
        try:
            # Cloudinary থেকে ইমেজ ডিলিট করুন
            cloudinary.uploader.destroy(category.image.public_id)
        except Exception as e:
            print('Cloudinary delete error...', e)

        # Django ফিল্ড থেকেও ডিলিট করুন
        category.image.delete(save=False)

    # Category অবজেক্ট ডিলিট করুন
    category.delete()

    # ডিলিট করার পর redirect করুন
    return redirect('category_list')		
	
def vendor_list_view(request):
	vendors = Vendor.objects.all()
	context = {
		'vendors': vendors,
	}
	return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
	vendor = Vendor.objects.get(vid=vid)
	products = Product.objects.filter(product_status='published', vendor=vendor)
	context = {
		'vendor': vendor,
		'products': products,
	}
	return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
	product = Product.objects.get(pid=pid)
	# product = get_object_or_404(Product, pid=pid)
	products = Product.objects.filter(category=product.category).exclude(pid=pid)
	p_image = product.p_images.all()

	reviews = ProductReview.objects.filter(product=product).order_by('-date')
	average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
	review_form = ProductReviewFrom()

	make_review = True
	if request.user.is_authenticated:
		user_review_count = ProductReview.objects.filter(user=request.user, product=product).count() 

		if user_review_count > 0:
			make_review = False

	context = {
		'product': product,
		'p_image': p_image,
		'products': products,
		'reviews': reviews,
		'average_rating': average_rating,
		'review_form': review_form,
		'make_review': make_review,
	}
	return render(request, 'core/product-detail.html', context)

def tags_list(request, tag_slug=None):
	products = Product.objects.filter(product_status='published').order_by('-id')

	tag = None
	if tag_slug:
		tag = Tag.objects.get(slug=tag_slug)
		# tag = get_object_or_404(Tag, slug=tag_slug)
		products = products.filter(tags__in=[tag])

	context = {
		'products': products,
		'tag': tag,
	}

	return render(request, 'core/tag.html', context)

def ajax_add_review(request, pid):
	product = Product.objects.get(pk=pid)
	user = request.user
	image = user.image.url

	review = ProductReview.objects.create(
		user=user,
		product=product,
		review=request.POST['review'],
		rating=request.POST['rating'],
	)
	
	context = {
		'user': user.username,
		'review': request.POST['review'],
		'rating': request.POST['rating'],
		'image': image
	}

	average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))


	return JsonResponse(
		{
			'bool': True,
			'context': context,
			'average_reviews': average_reviews,
		}
	)

def search_view(request):
	# query = request.GET['q'] OR
	query = request.GET.get('q') 

	products = Product.objects.filter(title__icontains=query).order_by('-date')

	context = {
		'products': products,
		'query': query,
	}

	return render(request, 'core/search.html', context)

def filter_product(request):
	categories = request.GET.getlist('category[]')
	vendors = request.GET.getlist('vendor[]')

	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')

	products = Product.objects.filter(product_status='published').order_by('-id').distinct()

	products = products.filter(price__gte=min_price)
	products = products.filter(price__lte=max_price)

	if len(categories) > 0:
		products = products.filter(category__id__in=categories).distinct()
	if len(vendors) > 0:
		products = products.filter(vendor__id__in=vendors).distinct()

	context = {
		'products': products
	}

	data = render_to_string('core/async/product-list.html', context)
	return JsonResponse({'data': data})


def add_to_cart(request):
    product_id = str(request.GET.get('id'))

    try:
        qty = int(request.GET.get('qty', 1))
    except (ValueError, TypeError):
        qty = 1

    try:
        price = float(request.GET.get('price', 0))
    except (ValueError, TypeError):
        price = 0.0

    cart_product = {
        product_id: {
            'qty': qty,
            'title': request.GET.get('title', ''),
            'price': price,
            'image': request.GET.get('image', ''),
            'pid': request.GET.get('pid', ''),
        }
    }

    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        if product_id in cart_data:
            cart_data[product_id]['qty'] += qty
        else:
            cart_data.update(cart_product)
        request.session['cart_data_object'] = cart_data
    else:
        request.session['cart_data_object'] = cart_product

    request.session.modified = True  # force save

    return JsonResponse({
        'data': request.session['cart_data_object'],
        'totalcartitems': len(request.session['cart_data_object'])
    })



def cart_view(request):
    cart_total_amount = 0
    cart_data = request.session.get('cart_data_object', {})
    
    for product_id, item in cart_data.items():
        try:
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0))
        except (ValueError, TypeError):
            qty, price = 0, 0
        cart_total_amount += qty * price

    context = {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
    }
    return render(request, 'core/cart.html', context)



def delete_from_cart(request):
    product_id = str(request.GET.get('id'))
    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_object'] = cart_data
            request.session.modified = True

    cart_total_amount = 0
    for pid, item in request.session.get('cart_data_object', {}).items():
        try:
            cart_total_amount += int(item['qty']) * float(item['price'])
        except (ValueError, TypeError):
            cart_total_amount += 0

    context = render_to_string('core/async/cart-list.html', {
        'cart_data': request.session.get('cart_data_object', {}),
        'totalcartitems': len(request.session.get('cart_data_object', {})),
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({
        'data': context,
        'totalcartitems': len(request.session.get('cart_data_object', {})),
    })


def update_cart(request):
    product_id = str(request.GET.get('id'))
    product_qty = int(request.GET.get('qty', 1))
    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        if product_id in cart_data:
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_object'] = cart_data
            request.session.modified = True

    cart_total_amount = 0
    for pid, item in request.session.get('cart_data_object', {}).items():
        try:
            cart_total_amount += int(item['qty']) * float(item['price'])
        except (ValueError, TypeError):
            cart_total_amount += 0

    context = render_to_string('core/async/cart-list.html', {
        'cart_data': request.session.get('cart_data_object', {}),
        'totalcartitems': len(request.session.get('cart_data_object', {})),
        'cart_total_amount': cart_total_amount
    })
    return JsonResponse({
        'data': context,
        'totalcartitems': len(request.session.get('cart_data_object', {})),
    })




@login_required
def checkout_view(request):
    cart = request.session.get('cart_data_object', {})
    if not cart:
        return redirect('core:cart')  # make sure 'cart' is named in urls.py

    subtotal = sum(Decimal(str(item['price'])) * int(item['qty']) for item in cart.values())
    shipping = Decimal('10.00') if subtotal > 0 else Decimal('0.00')
    total = subtotal + shipping

    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        country = request.POST.get('country', 'Bangladesh').strip()
        notes = request.POST.get('notes', '')

        errors = []
        if not full_name: errors.append("Full name is required")
        if not phone: errors.append("Phone number is required")
        if not address: errors.append("Address is required")

        if errors:
            return render(request, 'core/checkout.html', {
                'cart': cart,
                'subtotal': subtotal,
                'shipping': shipping,
                'total': total,
                'errors': errors,
                'form': {
                    'full_name': full_name, 'phone': phone, 'address': address,
                    'city': city, 'country': country, 'notes': notes
                }
            })

        # Save form data in session for initiate_payment
        form_data = {
            'full_name': full_name,
            'phone': phone,
            'address': address,
            'city': city,
            'country': country,
            'notes': notes
        }
        request.session['checkout_form'] = form_data

        with transaction.atomic():
            order = CartOrder.objects.create(
                user=request.user,
                price=total,
                paid_status=False,
                product_status="processing"
            )
            for pid, item in cart.items():
                CartOrderItems.objects.create(
                    order=order,
                    invoice_no=f"INV-{order.id}-{pid}",
                    product_status="processing",
                    item=item.get('title') ,
                    image=item.get('image', ''),
                    qty=int(item['qty']),
                    price=Decimal(str(item['price'])),
                    total=Decimal(str(item['price'])) * int(item['qty'])
                )

        request.session['cart_order_id'] = order.id
        request.session.pop('cart_data_object', None)

        return redirect('core:initiate_payment')  # or 'core:initiate_payment' if namespaced

    # GET request → no form_data needed
    return render(request, 'core/checkout.html', {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'form': {}   # empty dict avoids UnboundLocalError
    })



@login_required
def initiate_payment(request):
    order_id = request.session.get('cart_order_id')
    order = get_object_or_404(CartOrder, id=order_id, user=request.user)

    form = request.session.get('checkout_form', {})
    cart_total = order.price

    # Unique transaction ID
    tran_id = f"TXN-{order.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
    order.tran_id = tran_id
    order.save(update_fields=['tran_id'])

    sslcz = SSLCOMMERZ(settings.SSLCOMMERZ)

    # Callback URLs: sandbox vs production
    if settings.SSLCOMMERZ['issandbox']:
        success_url = request.build_absolute_uri('/payment/success/')
        fail_url    = request.build_absolute_uri('/payment/fail/')
        cancel_url  = request.build_absolute_uri('/payment/cancel/')
    else:
        success_url = "https://www.petukhotel.com/payment/success/"
        fail_url    = "https://www.petukhotel.com/payment/fail/"
        cancel_url  = "https://www.petukhotel.com/payment/cancel/"

    post_body = {
        'total_amount': str(cart_total),
        'currency': "BDT",
        'tran_id': tran_id,
        'success_url': success_url,
        'fail_url': fail_url,
        'cancel_url': cancel_url,
        'emi_option': 0,
        'cus_name': form.get('full_name') or request.user.get_full_name() or request.user.username,
        'cus_email': request.user.email or 'customer@example.com',
        'cus_phone': form.get('phone', ''),
        'cus_add1': form.get('address', ''),
        'cus_city': form.get('city', ''),
        'cus_country': form.get('country', 'Bangladesh'),
        'shipping_method': "NO",
        'num_of_item': order.cartorderitems_set.count(),
        'product_name': "Order Items",
        'product_category': "General",
        'product_profile': "general",
    }

    try:
        response = sslcz.createSession(post_body)
        if 'GatewayPageURL' not in response:
            messages.error(request, f"GatewayPageURL missing: {response}")
            return redirect('core:checkout')
        return redirect(response['GatewayPageURL'])
    except Exception as e:
        messages.error(request, f"Payment initiation failed: {e}")
        return redirect('core:checkout')


@csrf_exempt
def payment_success(request):
    data = request.POST.dict() if request.method == "POST" else request.GET.dict()
    val_id = data.get('val_id')
    tran_id = data.get('tran_id')

    sslcz = SSLCOMMERZ(settings.SSLCOMMERZ)
    try:
        validation = sslcz.validationTransactionOrder(val_id)
    except Exception as e:
        return render(request, "core/async/payment_fail.html", {"error": str(e)})

    # VALID এবং VALIDATED দুটোই success ধরুন
    if str(validation.get('status')).upper() in {"VALID", "VALIDATED"}:
        order = get_object_or_404(CartOrder, tran_id=tran_id)
        if str(order.price) == str(validation.get('amount')):
            order.paid_status = True
            order.product_status = "paid"
            order.save(update_fields=['paid_status', 'product_status'])
            return render(request, "core/async/payment_success.html", {"order": order, "response": validation})

    return render(request, "core/async/payment_fail.html", {"response": validation})



@csrf_exempt
def payment_fail(request):
    # Update status = "Cancelled"
    return render(request, "core/async/payment_fail.html")


@csrf_exempt
def payment_cancel(request):
    # Update status = "Cancelled"
    return render(request, "core/async/payment_cancel.html")

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(CartOrder, id=order_id, user=request.user)
    return render(request, 'core/async/order_success.html', {'order': order})





@login_required
def wishlist_view(request):
	try:
		wishlist = Wishlist.objects.filter(user=request.user)
	except:
		wishlist = None

	context = {
		'wishlist': wishlist
	}
	return render(request, 'core/wishlist.html', context)

@login_required
def add_to_wishlist(request):
	product_id = request.GET['id']
	product = Product.objects.get(id=product_id)

	context = {}

	wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()

	if wishlist_count > 0:
		context	= {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}
	else:
		new_wishlist = Wishlist.objects.create(
			product=product,
			user=request.user
		)
		context = {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}

	return JsonResponse(context)

def remove_from_wishlist(request):
	product_id = request.GET['id']
	wishlist = Wishlist.objects.filter(user=request.user)

	product = Wishlist.objects.get(id=product_id)
	product.delete()

	context = {
		'bool': True,
		'wishlist': wishlist
	}
	qs_json = serializers.serialize('json', wishlist)
	data = render_to_string('core/async/wishlist-list.html', context)
	return JsonResponse({'data': data, 'wishlist': qs_json})

def contact(request):
	return render(request, 'core/contact.html')

def ajax_contact_form(request):
	name = request.GET['name']
	email = request.GET['email']
	message = request.GET['message']

	contact = ContactUs.objects.create(
		name=name,		
		email=email,		
		message=message,		
	)

	data = {
		'bool': True,
	}

	return JsonResponse({'data': data})

def about(request):
	return render(request, 'core/about.html')

