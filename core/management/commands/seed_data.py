import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import (
    Product, Variant, Warehouse, Reseller, 
    WarehouseStock, StockMovement, Transaction, TransactionDetail,
    Invoice, Payment
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        # Order matters due to foreign keys
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        Transaction.objects.all().delete()
        StockMovement.objects.all().delete()
        WarehouseStock.objects.all().delete()
        Reseller.objects.all().delete()
        Variant.objects.all().delete()
        Product.objects.all().delete()
        Warehouse.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('Creating Users...'))
        # Create Reseller User
        reseller_user = User.objects.create_user(
            username='budi_reseller',
            email='budi@example.com',
            password='password123'
        )

        self.stdout.write(self.style.SUCCESS('Creating Warehouses...'))
        gudang_pusat = Warehouse.objects.create(name="Gudang Pusat (JKT)", location="Jakarta")
        gudang_sub = Warehouse.objects.create(name="Gudang Cabang (SBY)", location="Surabaya")

        self.stdout.write(self.style.SUCCESS('Creating Products & Variants...'))
        # Product 1: Kaos Polos
        p1 = Product.objects.create(name="Kaos Polos Premium", category="Atasan", brand="LocalBrand")
        v1_s = Variant.objects.create(product=p1, sku="KPO-BLK-S", color="Black", size="S", default_price=50000)
        v1_m = Variant.objects.create(product=p1, sku="KPO-BLK-M", color="Black", size="M", default_price=50000)
        v1_l = Variant.objects.create(product=p1, sku="KPO-BLK-L", color="Black", size="L", default_price=55000)

        # Product 2: Celana Chino
        p2 = Product.objects.create(name="Celana Chino Slim", category="Bawahan", brand="LocalBrand")
        v2_30 = Variant.objects.create(product=p2, sku="CHN-KHK-30", color="Khaki", size="30", default_price=120000)
        v2_32 = Variant.objects.create(product=p2, sku="CHN-KHK-32", color="Khaki", size="32", default_price=120000)

        # Product 3: Jaket Hoodie
        p3 = Product.objects.create(name="Hoodie Oversize", category="Outerwear", brand="StreetStyle")
        v3_all = Variant.objects.create(product=p3, sku="HOD-NVY-ALL", color="Navy", size="All Size", default_price=150000)

        variants = [v1_s, v1_m, v1_l, v2_30, v2_32, v3_all]

        self.stdout.write(self.style.SUCCESS('Creating Resellers...'))
        # Reseller 1 (Linked to User)
        r1 = Reseller.objects.create(
            user=reseller_user,
            name="Budi Store (Official)",
            phone="08123456789",
            address="Jl. Sudirman No. 1, Jakarta",
            credit_limit=10000000
        )
        
        # Reseller 2 (Manual/Offline)
        r2 = Reseller.objects.create(
            name="Toko Sejahtera (Offline)",
            phone="08987654321",
            address="Pasar Tanah Abang Blok A",
            credit_limit=5000000
        )

        self.stdout.write(self.style.SUCCESS('Initializing Stock...'))
        # Add Initial Stock via "Logic" (Movement IN)
        # We simulate this manually to trigger the logic or just create objects
        # Better to create objects directly for seeding speed, but mirroring logic is safer
        
        for v in variants:
            # Stock at Pusat
            qty_pusat = random.randint(50, 100)
            WarehouseStock.objects.create(warehouse=gudang_pusat, variant=v, qty_available=qty_pusat)
            StockMovement.objects.create(
                warehouse=gudang_pusat, variant=v, movement_type='IN', 
                qty=qty_pusat, ref_type='ADJUST', user=User.objects.first() # Admin
            )

            # Stock at Cabang
            qty_cabang = random.randint(10, 30)
            WarehouseStock.objects.create(warehouse=gudang_sub, variant=v, qty_available=qty_cabang)
            StockMovement.objects.create(
                warehouse=gudang_sub, variant=v, movement_type='IN', 
                qty=qty_cabang, ref_type='ADJUST', user=User.objects.first()
            )

        self.stdout.write(self.style.SUCCESS('Creating Transactions...'))
        
        # TRX 1: Finalized (Budi buys Kaos & Chino)
        trx1 = Transaction.objects.create(
            reseller=r1,
            warehouse=gudang_pusat,
            user=reseller_user,
            status='DRAFT' # Will finalize below
        )
        
        # Add details
        TransactionDetail.objects.create(transaction=trx1, variant=v1_m, qty=10, price=v1_m.default_price, subtotal=10*v1_m.default_price)
        TransactionDetail.objects.create(transaction=trx1, variant=v2_32, qty=5, price=v2_32.default_price, subtotal=5*v2_32.default_price)
        
        # Finalize TRX 1
        trx1.status = 'FINAL'
        trx1.save() # Signals will run: Stock OUT, Invoice Created, Reseller Debt Added

        # TRX 2: Draft (Toko Sejahtera buys Hoodie)
        trx2 = Transaction.objects.create(
            reseller=r2,
            warehouse=gudang_pusat,
            user=User.objects.first(), # Admin created this
            status='DRAFT'
        )
        TransactionDetail.objects.create(transaction=trx2, variant=v3_all, qty=20, price=v3_all.default_price, subtotal=20*v3_all.default_price)

        self.stdout.write(self.style.SUCCESS('Simulating Payments...'))
        # Budi pays half of his invoice
        # Find Budi's invoice
        inv1 = Invoice.objects.get(transaction=trx1)
        
        Payment.objects.create(
            reseller=r1,
            invoice=inv1,
            amount=inv1.total_amount / 2,
            method="Transfer BCA"
        ) # Signal will run: Update Invoice status, Reduce Reseller Debt

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded data!'))
        self.stdout.write(f'  - Products: {Product.objects.count()}')
        self.stdout.write(f'  - Variants: {Variant.objects.count()}')
        self.stdout.write(f'  - Warehouses: {Warehouse.objects.count()}')
        self.stdout.write(f'  - Resellers: {Reseller.objects.count()}')
        self.stdout.write(f'  - Transactions: {Transaction.objects.count()}')
        self.stdout.write(f'  - Invoices: {Invoice.objects.count()}')
        self.stdout.write(f'  - User: budi_reseller / password123')
