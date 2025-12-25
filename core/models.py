from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from shortuuid.django_fields import ShortUUIDField
from cloudinary.models import CloudinaryField

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    ( 1, "★☆☆☆☆"),
    ( 2, "★★☆☆☆"),
    ( 3, "★★★☆☆"),
    ( 4, "★★★★☆"),
    ( 5, "★★★★★"),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat', alphabet='abcdefgh12345')
    title = models.CharField(max_length=100, default="Category Name")
    image = CloudinaryField('image', folder='petuk-hotel/category/', default="category.jpg")

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title

    # update category
    def save(self, *args, **kwargs):
        # যদি অবজেক্ট আগে থেকেই থাকে এবং নতুন ইমেজ সেট করা হয়
        if self.pk:
            old_category = Category.objects.filter(pk=self.pk).first()
            if old_category and old_category.image != self.image:
                try:
                    import cloudinary.uploader
                    cloudinary.uploader.destroy(old_category.image.public_id)
                except Exception as e:
                    print("Cloudinary delete error...", e)

        super().save(*args, **kwargs)

    # delete category
    def delete(self, *args, **kwargs):
        if self.image:
            try:
                import cloudinary.uploader
                cloudinary.uploader.destroy(self.image.public_id)
            except Exception as e:
                print('Cloudinary delete error ...', e)

        super().delete(*args, **kwargs)		


class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='ven', alphabet='abcdefgh12345')
    
    title = models.CharField(max_length=100, default="Vendor Name")
    image = CloudinaryField('image',folder='petuk-hotel/vendor/', default="vendor.jpg")
    description = CKEditor5Field( config_name='default', null=True, blank=True, default="Vendor Description" )

    address = models.CharField(max_length=100, default="123 Main Street")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    email = models.CharField(max_length=100, default="example@mail.com")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title


    # update vendor
    def save(self, *args, **kwargs):
        # যদি অবজেক্ট আগে থেকেই থাকে এবং নতুন ইমেজ সেট করা হয়
        if self.pk:
            old_vendor = Vendor.objects.filter(pk=self.pk).first()
            if old_vendor and old_vendor.image != self.image:
                try:
                    import cloudinary.uploader
                    cloudinary.uploader.destroy(old_vendor.image.public_id)
                except Exception as e:
                    print("Cloudinary delete error...", e)

        super().save(*args, **kwargs)

    # delete category
    def delete(self, *args, **kwargs):
        if self.image:
            try:
                import cloudinary.uploader
                cloudinary.uploader.destroy(self.image.public_id)
            except Exception as e:
                print('Cloudinary delete error ...', e)

        super().delete(*args, **kwargs)	    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet='abcdefgh12345')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

    title = models.CharField(max_length=100, default="Product Name")
    image = CloudinaryField('image', folder='petuk-hotel/product/', default="product.jpg")
    description = CKEditor5Field( config_name='default', null=True, blank=True, default="Product Description" )

    price = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=50)

    specifications = CKEditor5Field( config_name='default', null=True, blank=True )
    stock_count = models.PositiveIntegerField(default=10, null=True, blank=True)
    shipping = models.CharField(max_length=100, default=1, null=True, blank=True)
    weight = models.CharField(max_length=100, default=0.5, null=True, blank=True)
    life = models.CharField(max_length=100, default=10, null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=30, prefix="sku", alphabet='1234567890')

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_product = Product.objects.filter(pk=self.pk).first()
            if old_product and old_product.image and old_product.image != self.image:
                try:
                    import cloudinary.uploader
                    cloudinary.uploader.destroy(old_product.image.public_id)
                except Exception as e:
                    print("Cloudinary delete error...", e)

        super().save(*args, **kwargs)


    # delete category
    def delete(self, *args, **kwargs):
        if self.image:
            try:
                import cloudinary.uploader
                cloudinary.uploader.destroy(self.image.public_id)
            except Exception as e:
                print('Cloudinary delete error ...', e)

        super().delete(*args, **kwargs)	


    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'



####### Cart, Order #######



class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    tran_id = models.CharField(max_length=64, blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = 'Cart Order'

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50">' % (self.image))



####### Product Review, Wishlist, Address #######



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'



####### Contact, Profile #######



class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.name
