from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Inventory
    path('inventory/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventory/in/', views.StockInView.as_view(), name='stock_in'),

    # Transaction
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),

    # Finance
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/pay/', views.PaymentCreateView.as_view(), name='payment_create'),

    # Returns
    path('returns/', views.ReturnListView.as_view(), name='return_list'),
    path('returns/create/', views.ReturnCreateView.as_view(), name='return_create'),
    path('returns/<int:pk>/', views.ReturnDetailView.as_view(), name='return_detail'),

    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

    # Scanner & Codes
    path('scanner/', views.scanner, name='scanner'),
    path('scanner/advanced/', views.scanner_advanced, name='scanner_advanced'),
    path('scanner/process/', views.process_scanned_data, name='process_scanned_data'),
    path('variants/<int:pk>/', views.VariantDetailView.as_view(), name='variant_detail'),
    path('variants/<int:pk>/barcode/', views.variant_barcode, name='variant_barcode'),
    path('invoices/<int:pk>/qrcode/', views.invoice_qrcode, name='invoice_qrcode'),
    path('scan-lookup/', views.scan_lookup, name='scan_lookup'),
]
