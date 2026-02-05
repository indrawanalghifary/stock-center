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

                total_return_value = 0 # Need to calculate value based on original price if possible, or just qty logic

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
                        # user=instance.user # ReturnHeader doesn't have user yet, assumed context
                    )
                    
                    # Calculate refund value? 
                    # For now, let's assume we credit based on default price or logic needs price in ReturnDetail.
                    # Since ReturnDetail doesn't have price, we might check original transaction or Variant default price.
                    # Using Variant default price for now as safe fallback or 0 if strictly qty.
                    # Backend.md says: "Retur FINAL -> StockMovement RETURN, tambah WarehouseStock, kurangi invoice"
                    # But reducing specific invoice might be complex if invoice is already paid.
                    # Let's credit the Reseller Balance directly for flexibility.
                    
                    value = detail.variant.default_price * detail.qty
                    total_return_value += value

                # 4. Update Reseller Balance (Credit/Reduce Debt)
                instance.reseller.current_balance -= total_return_value
                instance.reseller.save()
