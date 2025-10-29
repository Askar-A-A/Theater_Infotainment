from django.urls import path
from . import views

app_name = "theater_payments"

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('create-payment/', views.create_qr_payment, name='create_qr_payment'),
    path('payment/<str:session_id>/', views.qr_payment_display, name='qr_payment_display'),
]