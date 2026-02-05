from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 🧩 1️⃣ MASTER DATA

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True, help_text="QR Code content")
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    default_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.sku} ({self.color}/{self.size})"

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Reseller(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class ResellerPrice(models.Model):
    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, related_name='special_prices')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    custom_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('reseller', 'variant')

# 📦 2️⃣ STOK SYSTEM

class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    qty_available = models.IntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'variant')

    def __str__(self):
        return f"{self.warehouse.name} - {self.variant.sku}: {self.qty_available}"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Inbound'),
        ('OUT', 'Outbound'),
        ('RETURN', 'Return'),
        ('ADJUST', 'Adjustment'),
    ]

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    qty = models.IntegerField(help_text="Positive for IN/RETURN, Negative for OUT/ADJUST")
    ref_type = models.CharField(max_length=50, help_text="TRX, RETURN, OPNAME")
    ref_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.variant.sku} ({self.qty})"

# 🧾 3️⃣ TRANSAKSI PENGAMBILAN RESELLER

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
    ]

    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TRX-{self.id} - {self.reseller.name}"

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='details')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.qty * self.price
        super().save(*args, **kwargs)

# 💰 4️⃣ PIUTANG (ACCOUNT RECEIVABLE)

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]

    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"INV-{self.id} - {self.reseller.name}"

class Payment(models.Model):
    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

# 🔁 5️⃣ RETUR BARANG

class ReturnHeader(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
    ]

    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RET-{self.id} - {self.reseller.name}"

class ReturnDetail(models.Model):
    return_header = models.ForeignKey(ReturnHeader, on_delete=models.CASCADE, related_name='details')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    qty = models.IntegerField()
