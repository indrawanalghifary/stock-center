from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import (
    Transaction, TransactionDetail, WarehouseStock, StockMovement,
    Invoice, Payment, ReturnHeader, ReturnDetail, Reseller
)

@receiver(pre_save, sender=Transaction)
def transaction_finalized(sender, instance, **kwargs):
    """
    Handles logic when a Transaction is moved from DRAFT to FINAL.
    1. Validates stock availability.
    2. Deducts stock.
    3. Creates StockMovement (OUT).
    4. Creates Invoice.
    5. Updates Reseller balance.
    """
    if instance.pk:
        old_instance = Transaction.objects.get(pk=instance.pk)
        if old_instance.status == 'DRAFT' and instance.status == 'FINAL':
            with transaction.atomic():
                details = instance.details.all()
                if not details.exists():
                     raise ValidationError("Cannot finalize a transaction with no items.")

                total_amount = 0
                
                for detail in details:
                    # 1. Get Stock
                    stock, created = WarehouseStock.objects.get_or_create(
                        warehouse=instance.warehouse,
                        variant=detail.variant
                    )
                    
                    # 2. Validate Stock
                    if stock.qty_available < detail.qty:
                        raise ValidationError(f"Insufficient stock for {detail.variant}. Available: {stock.qty_available}, Requested: {detail.qty}")
                    
                    # 3. Deduct Stock
                    stock.qty_available -= detail.qty
                    stock.save()

                    # 4. Create Stock Movement
                    StockMovement.objects.create(
                        warehouse=instance.warehouse,
                        variant=detail.variant,
                        movement_type='OUT',
                        qty=-detail.qty,
                        ref_type='TRX',
                        ref_id=instance.id,
                        user=instance.user
                    )
                    
                    total_amount += detail.subtotal

                # 5. Create Invoice
                invoice = Invoice.objects.create(
                    reseller=instance.reseller,
                    transaction=instance,
                    total_amount=total_amount,
                    status='UNPAID'
                )

                # 6. Update Reseller Balance (Add Debt)
                instance.reseller.current_balance += total_amount
                instance.reseller.save()

@receiver(post_save, sender=Payment)
def payment_received(sender, instance, created, **kwargs):
    """
    Handles logic when a Payment is created.
    1. Updates Invoice paid_amount and status.
    2. Updates Reseller balance (Reduce Debt).
    """
    if created:
        with transaction.atomic():
            invoice = instance.invoice
            invoice.paid_amount += instance.amount
            
            if invoice.paid_amount >= invoice.total_amount:
                invoice.status = 'PAID'
            elif invoice.paid_amount > 0:
                invoice.status = 'PARTIAL'
            
            invoice.save()

            # Update Reseller Balance (Reduce Debt)
            reseller = instance.reseller
            reseller.current_balance -= instance.amount
            reseller.save()

@receiver(pre_save, sender=ReturnHeader)
def return_finalized(sender, instance, **kwargs):
    """
    Handles logic when a ReturnHeader is moved from DRAFT to FINAL.
    1. Adds stock back.
    2. Creates StockMovement (RETURN).
    3. Updates Reseller balance (Credit).
    """
    if instance.pk:
        old_instance = ReturnHeader.objects.get(pk=instance.pk)
        if old_instance.status == 'DRAFT' and instance.status == 'FINAL':
            with transaction.atomic():
                details = instance.details.all()
                if not details.exists():
                     raise ValidationError("Cannot finalize a return with no items.")

                total_return_value = 0
                original_transaction = instance.invoice.transaction

                for detail in details:
                    # 1. Get Stock
                    stock, created = WarehouseStock.objects.get_or_create(
                        warehouse=instance.warehouse,
                        variant=detail.variant
                    )

                    # 2. Add Stock
                    stock.qty_available += detail.qty
                    stock.save()

                    # 3. Create Stock Movement
                    StockMovement.objects.create(
                        warehouse=instance.warehouse,
                        variant=detail.variant,
                        movement_type='RETURN',
                        qty=detail.qty,
                        ref_type='RETURN',
                        ref_id=instance.id,
                        user=None # Signal doesn't have easy access to request.user
                    )
                    
                    # 4. Calculate Refund Value based on ORIGINAL Transaction Price
                    # Find the specific item in the original transaction
                    original_item = original_transaction.details.filter(variant=detail.variant).first()
                    
                    if original_item:
                        price_to_refund = original_item.price
                    else:
                        # Fallback if not found (should be rare)
                        price_to_refund = detail.variant.default_price
                    
                    value = price_to_refund * detail.qty
                    total_return_value += value

                # 5. Create Payment Record (Treat Return as Payment)
                # This ensures the Invoice status is updated to PAID/PARTIAL correctly
                # and the Reseller Balance is reduced via the payment_received signal.
                Payment.objects.create(
                    reseller=instance.reseller,
                    invoice=instance.invoice,
                    amount=total_return_value,
                    method="RETURN_ADJUSTMENT"
                )

                # Note: We removed the manual deduction of reseller.current_balance here
                # because creating the Payment object triggers 'payment_received' 
                # which handles the deduction. Prevents double counting.
