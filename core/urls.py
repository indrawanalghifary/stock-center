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
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('transactions/<int:pk>/detail/<int:detail_pk>/edit/', views.TransactionDetailUpdateView.as_view(), name='transaction_detail_update'),
    path('transactions/<int:pk>/detail/<int:detail_pk>/delete/', views.TransactionDetailDeleteView.as_view(), name='transaction_detail_delete'),

    # Finance
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/pay/', views.PaymentCreateView.as_view(), name='payment_create'),

    # Returns
    path('returns/', views.ReturnListView.as_view(), name='return_list'),
    path('returns/create/', views.ReturnCreateView.as_view(), name='return_create'),
    path('returns/<int:pk>/', views.ReturnDetailView.as_view(), name='return_detail'),

    # Packing
    path('packing/', views.PackingListView.as_view(), name='packing_list'),

    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('analysis/reseller-sku/', views.ResellerSkuAnalysisView.as_view(), name='reseller_sku_analysis'),

    # Master Data
    path('master/', views.master_data_dashboard, name='master_dashboard'),
    
    # Users
    path('master/users/', views.UserListView.as_view(), name='user_list'),
    path('master/users/add/', views.UserCreateView.as_view(), name='user_create'),
    path('master/users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('master/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Resellers
    path('master/resellers/', views.ResellerListView.as_view(), name='reseller_list'),
    path('master/resellers/add/', views.ResellerCreateView.as_view(), name='reseller_create'),
    path('master/resellers/<int:pk>/', views.ResellerDetailView.as_view(), name='reseller_detail'),
    path('master/resellers/<int:pk>/edit/', views.ResellerUpdateView.as_view(), name='reseller_update'),
    path('master/resellers/<int:pk>/delete/', views.ResellerDeleteView.as_view(), name='reseller_delete'),

    # Warehouses
    path('master/warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('master/warehouses/add/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('master/warehouses/<int:pk>/edit/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('master/warehouses/<int:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),

    # Products & Variants
    path('master/products/', views.ProductListView.as_view(), name='product_list'),
    path('master/products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('master/products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('master/products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('master/products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    path('master/variants/add/', views.VariantCreateView.as_view(), name='variant_create'),
    path('master/variants/<int:pk>/edit/', views.VariantUpdateView.as_view(), name='variant_update'),
    path('master/variants/<int:pk>/delete/', views.VariantDeleteView.as_view(), name='variant_delete'),

    # Reseller Prices
    path('master/reseller-prices/', views.ResellerPriceListView.as_view(), name='reseller_price_list'),
    path('master/reseller-prices/add/', views.ResellerPriceCreateView.as_view(), name='reseller_price_create'),
    path('master/reseller-prices/<int:pk>/edit/', views.ResellerPriceUpdateView.as_view(), name='reseller_price_update'),
    path('master/reseller-prices/<int:pk>/delete/', views.ResellerPriceDeleteView.as_view(), name='reseller_price_delete'),

    # Scanner & Codes
    path('scanner/', views.scanner, name='scanner'),
    path('scanner/advanced/', views.scanner_advanced, name='scanner_advanced'),
    path('scanner/process/', views.process_scanned_data, name='process_scanned_data'),
    path('variants/<int:pk>/', views.VariantDetailView.as_view(), name='variant_detail'),
    path('variants/<int:pk>/barcode/', views.variant_barcode, name='variant_barcode'),
    path('variants/bulk-barcode/', views.bulk_barcode, name='bulk_barcode'),
    path('invoices/<int:pk>/qrcode/', views.invoice_qrcode, name='invoice_qrcode'),
    path('scan-lookup/', views.scan_lookup, name='scan_lookup'),
    
    # API
    path('api/variants/<int:variant_id>/', views.api_variant_detail, name='api_variant_detail'),
]
