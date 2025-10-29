from django.db import models
from django.utils import timezone
import uuid

class MenuItem(models.Model):
    """Food and beverage items available for purchase"""
    CATEGORY_CHOICES = [
        ('ticket', 'Ticket'),
        ('beverage', 'Beverage'),
        ('snack', 'Snack'),
        ('merchandise', 'Merchandise'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class QRPaymentSession(models.Model):
    """Payment session tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    qr_code_data = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Optional customer info
    customer_name = models.CharField(max_length=200, blank=True)
    customer_email = models.EmailField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment Session"
        verbose_name_plural = "Payment Sessions"
    
    def __str__(self):
        return f"Payment {self.session_id} - ${self.total_amount} ({self.status})"
    
    def is_expired(self):
        return timezone.now() > self.expires_at and self.status == 'pending'

class OrderItem(models.Model):
    """Items in an order"""
    payment_session = models.ForeignKey(QRPaymentSession, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
