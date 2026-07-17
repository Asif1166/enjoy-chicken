from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from django.utils import timezone
# Create your models here.
from django.utils.html import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.fields import RichTextField

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class SuperCategory(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="supercat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="supercategory", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Super Categories'
        
    def super_category_img(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Category(models.Model):
    super_category = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL, null=True)
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def category_img(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="subcat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="sub_category", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Sub Categories'
    


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    eng_description = models.TextField(blank=True, null=True)
    
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    chat_resp_time = models.CharField(max_length=100, blank=True, null=True)
    shipping_on_time = models.CharField(max_length=100, blank=True, null=True)
    days_return = models.CharField(max_length=100, blank=True, null=True)
    warranty_period = models.CharField(max_length=100, blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    class Meta:
        verbose_name_plural = 'Vendors'
        
    def vendor_img(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

STATUS_CHOICE = (
("progress", "Order In Progress"),
("placed", "Order Placed"),
("accepted", "Order Accepted"),

("delivered", "Order Delivered"),
("cancelled", "Order Cancelled"),

)

STATUS = (
("draft", "Draft"),
("disabled", "Disabled"),
("rejected", "Rejected"),
("in_review", "In Review"),
("published", "Published"),
)

ORDER_TYPE = (
("delivery", "Delivery"),
("take_away", "Take Away"),
("pay_on_spot", "Pay On Spot")
)

RATING = (
(1, "⭐☆☆☆☆☆"),
(2, "⭐⭐☆☆☆"),
(3, "⭐⭐⭐☆☆"),
(4, "⭐⭐⭐⭐☆"),
(5, "⭐⭐⭐⭐⭐"),
)


class Countdown(models.Model):
    event_name = models.CharField(max_length=200, blank=True, null=True)
    eng_event_name = models.CharField(max_length=200, blank=True, null=True)
    percentage = models.IntegerField(default=0)
    target_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_past_due(self):
        return timezone.now() > self.target_date

    def __str__(self):
        return f"{self.event_name} - {self.target_date.strftime('%d/%m/%Y %H:%M:%S')}"
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=100, blank=True, null=True)
    eng_title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    eng_description = RichTextField(blank=True, null=True)
    
    offer_price = models.DecimalField(max_digits=99999999999, decimal_places=2,  blank=True, null=True)
    price = models.DecimalField(max_digits=99999999999, decimal_places=2,  blank=True, null=True)
    old_price = models.DecimalField(max_digits=9999999999, decimal_places=2,  blank=True, null=True)
    
    specifications = models.TextField(blank=True, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=100, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)

    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix="sku", alphabet="abcdefgh12345")
    
    quantity = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    type = models.CharField(max_length=100, default="Organic")
    
    offer_countdown = models.ForeignKey(Countdown, on_delete=models.SET_NULL, null=True, blank=True)

    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    tax_applied = models.BooleanField(default=False)
    offer_applied = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Products'
        
    
    def __str__(self):
        return self.title
    
    def product_img(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "(No image)"
    
    
    def save(self, *args, **kwargs):
        # Calculate the price based on the percentage and old price
        if not self.price and self.old_price and self.percentage:
            old_price_decimal = Decimal(self.old_price)
            percentage_decimal = Decimal(self.percentage) / Decimal(100)
            self.price = old_price_decimal * (1 - percentage_decimal)
        
        # Calculate the percentage if price and old_price are provided
        if self.price and self.old_price:
            old_price_decimal = Decimal(self.old_price)
            price_decimal = Decimal(self.price)
            self.percentage = int(((old_price_decimal - price_decimal) / old_price_decimal) * 100)
        
        # Update offer_price in the related Countdown model
        if self.offer_countdown and not self.offer_applied :
            countdown_percentage = Decimal(self.offer_countdown.percentage)
            self.percentage = int(countdown_percentage)  # Sync Countdown percentage with Product
            
            # Calculate offer_price using Countdown percentage
            countdown_discount = countdown_percentage / Decimal(100)
            self.old_price = self.price
            self.price = self.price * (1 - countdown_discount)
            self.offer_applied = True
            
            # Save the Countdown instance if necessary
            self.offer_countdown.save()

        # Call the superclass save method
        super(Product, self).save(*args, **kwargs)


    
class ProductImages(models.Model):
    image = models.ImageField(upload_to="category", blank=True, null=True)
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = 'Product Images'
        
    

# cart section
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    order_notes = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Shipping Address'

class CostSettings(models.Model):
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Default shipping cost")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tax rate as a percentage, e.g., 15 for 15%")

    def __str__(self):
        return f"Shipping: {self.shipping_cost}, Tax Rate: {self.tax_rate}%"

    class Meta:
        verbose_name_plural = "Cost Settings"
    
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=99999999999, decimal_places=2,  blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=100, default="placed")
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    tax_amount = models.CharField(max_length=10, blank=True, null=True)
    processed= models.BooleanField(default=False)

    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)


    order_type = models.CharField(choices=ORDER_TYPE, max_length=100, default="delivery")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Cart Order'


@receiver(post_save, sender=CartOrder)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user if instance.user else None,  # Set to None for anonymous users
            title='New Order Created',
            details=f'Your order #{instance.id} has been successfully created. Total Price: {instance.price}',
            avatar=None  # Optional: Set an avatar if needed
        )

    
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=100, default="process")
    item = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    qty = models.IntegerField(default=0)
    
    
    price = models.DecimalField(max_digits=99999999999, decimal_places=2,  blank=True, null=True)
    total = models.DecimalField(max_digits=9999999999, decimal_places=2,  blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
    
    

    
# product review

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    

    
    class Meta:
        verbose_name_plural = 'Product Reviews'
        
    def __str__(self):
        return self.review
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    

    
    class Meta:
        verbose_name_plural = 'Wishlists'
        
    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Address'
        

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Associate notification with a user
    title = models.CharField(max_length=255)  # Title of the notification
    details = models.TextField()  # Detailed message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notification is created
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Optional avatar image
    class Meta:
        ordering = ['-created_at']  # Order notifications by newest first

    def __str__(self):
        return f"{self.title}"  # String representation of the notification