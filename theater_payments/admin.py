from django.contrib import admin
from .models import MenuItem, QRPaymentSession, OrderItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'sort_order']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available', 'sort_order']
    ordering = ['sort_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Display Options', {
            'fields': ('image', 'is_available', 'sort_order')
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['menu_item', 'quantity', 'unit_price', 'total_price']

@admin.register(QRPaymentSession)
class QRPaymentSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'total_amount', 'status', 'created_at', 'customer_name']
    list_filter = ['status', 'created_at']
    search_fields = ['session_id', 'customer_name', 'customer_email']
    readonly_fields = ['session_id', 'qr_code_data', 'created_at', 'expires_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('session_id', 'total_amount', 'status', 'qr_code_data')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'completed_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manual creation of payment sessions through admin
        return False

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['payment_session', 'menu_item', 'quantity', 'unit_price', 'total_price']
    list_filter = ['menu_item__category', 'payment_session__status']
    search_fields = ['menu_item__name', 'payment_session__session_id']
    readonly_fields = ['total_price']
    
    def has_add_permission(self, request):
        # Prevent manual creation of order items through admin
        return False