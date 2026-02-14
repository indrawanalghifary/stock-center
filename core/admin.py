from django.contrib import admin
from .models import (
    Product, Variant, Warehouse, Reseller, ResellerPrice,
    WarehouseStock, StockMovement, Transaction, TransactionDetail,
    Invoice, Payment, ReturnHeader, ReturnDetail,
    PackingTask, PackingItem
)

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 10

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'is_active')
    search_fields = ('name', 'category', 'brand')
    inlines = [VariantInline]

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')

@admin.register(Reseller)
class ResellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'credit_limit', 'current_balance')
    search_fields = ('name', 'phone')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'variant', 'movement_type', 'qty', 'created_at')
    list_filter = ('movement_type', 'warehouse', 'created_at')

class TransactionDetailInline(admin.TabularInline):
    model = TransactionDetail
    extra = 0

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'reseller', 'warehouse', 'status', 'created_at')
    list_filter = ('status', 'warehouse')
    inlines = [TransactionDetailInline]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'reseller', 'total_amount', 'paid_amount', 'status')
    list_filter = ('status',)

admin.site.register(WarehouseStock)
admin.site.register(ResellerPrice)
admin.site.register(Payment)
admin.site.register(ReturnHeader)
admin.site.register(ReturnDetail)

class PackingItemInline(admin.TabularInline):
    model = PackingItem
    extra = 0
    readonly_fields = ('variant', 'qty')

@admin.register(PackingTask)
class PackingTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'warehouse', 'total_items', 'total_fee', 'created_at')
    list_filter = ('warehouse', 'user', 'created_at')
    search_fields = ('user__username', 'warehouse__name')
    readonly_fields = ('created_at',)
    inlines = [PackingItemInline]