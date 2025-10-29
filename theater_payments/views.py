from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import qrcode
import io
import base64
import uuid
import json
from .models import MenuItem, QRPaymentSession, OrderItem

def menu_view(request):
    """Display available menu items"""
    menu_items = MenuItem.objects.filter(is_available=True).order_by('category', 'sort_order')
    
    # Group by category
    menu_by_category = {}
    for item in menu_items:
        if item.category not in menu_by_category:
            menu_by_category[item.category] = []
        menu_by_category[item.category].append(item)
    
    return render(request, 'theater_payments/menu.html', {
        'menu_by_category': menu_by_category
    })

def create_qr_payment(request):
    """Create a new QR payment session"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        # Parse order data from request
        items_data = json.loads(request.POST.get('items', '[]'))
        customer_name = request.POST.get('customer_name', '')
        customer_email = request.POST.get('customer_email', '')
        
        if not items_data:
            return JsonResponse({'error': 'No items selected'}, status=400)
        
        # Create payment session
        session_id = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(minutes=15)  # 15 minute expiry
        
        payment_session = QRPaymentSession.objects.create(
            session_id=session_id,
            expires_at=expires_at,
            customer_name=customer_name,
            customer_email=customer_email,
            total_amount=0,  # Will calculate below
            qr_code_data=f"THEATER_PAY:{session_id}"
        )
        
        total_amount = 0
        
        # Process each item
        for item_data in items_data:
            menu_item = get_object_or_404(MenuItem, id=item_data['id'])
            quantity = int(item_data['quantity'])
            
            OrderItem.objects.create(
                payment_session=payment_session,
                menu_item=menu_item,
                quantity=quantity,
                unit_price=menu_item.price
            )
            total_amount += menu_item.price * quantity
        
        # Update total amount
        payment_session.total_amount = total_amount
        payment_session.save()
        
        return JsonResponse({
            'success': True,
            'session_id': session_id,
            'total_amount': str(total_amount),
            'expires_at': expires_at.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def qr_payment_display(request, session_id):
    """Display QR code for payment"""
    payment_session = get_object_or_404(QRPaymentSession, session_id=session_id)
    
    if payment_session.status != 'pending':
        return render(request, 'theater_payments/payment_error.html', {
            'error': f'Payment is {payment_session.status}'
        })
    
    # Check if expired
    if payment_session.is_expired():
        payment_session.status = 'expired'
        payment_session.save()
        return render(request, 'theater_payments/payment_error.html', {
            'error': 'Payment session has expired'
        })
    
    # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payment_session.qr_code_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_image_data = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'theater_payments/qr_payment.html', {
        'payment_session': payment_session,
        'qr_image_data': qr_image_data,
        'items': payment_session.items.all()
    })
