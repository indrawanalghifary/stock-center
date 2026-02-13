from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django import forms
from .models import WarehouseStock, StockMovement, Variant, Warehouse, Transaction, TransactionDetail, Invoice, Payment, ReturnHeader, ReturnDetail, Product, ResellerPrice
from .forms import StockAdjustmentForm, TransactionCreateForm, TransactionDetailForm

@login_required
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    context = {}
    
    # Check if user is a Reseller
    is_reseller = hasattr(request.user, 'reseller_profile')
    
    if is_reseller:
        reseller = request.user.reseller_profile
        # Reseller Stats
        # Balance / Debt
        context['reseller_balance'] = reseller.current_balance
        
        # Unpaid Invoices
        context['unpaid_invoices_count'] = Invoice.objects.filter(
            reseller=reseller, 
            status__in=['UNPAID', 'PARTIAL']
        ).count()
        
        # Active Transactions
        context['active_transactions'] = Transaction.objects.filter(
            reseller=reseller,
            status='DRAFT'
        ).count()

        # Draft Returns
        context['draft_returns_count'] = ReturnHeader.objects.filter(
            reseller=reseller,
            status='DRAFT'
        ).count()
        
        context['is_reseller'] = True
        
    else:
        # Admin Stats (Global)
        stock_count = WarehouseStock.objects.aggregate(total=Sum('qty_available'))['total'] or 0
        
        total_receivables = Invoice.objects.filter(status__in=['UNPAID', 'PARTIAL']).aggregate(
            total=Sum('total_amount'), 
            paid=Sum('paid_amount')
        )
        receivables_value = (total_receivables['total'] or 0) - (total_receivables['paid'] or 0)
        
        transaction_count = Transaction.objects.filter(created_at__date=timezone.now().date()).count()
        
        # Pending Returns
        pending_returns = ReturnHeader.objects.filter(status='DRAFT').count()

        context.update({
            'stock_count': stock_count,
            'receivables_value': receivables_value,
            'transaction_count': transaction_count,
            'pending_returns': pending_returns,
            'is_reseller': False
        })

    return render(request, 'home.html', context)


def login_view(request):
    pass

# ... (Previous Views) ...

@method_decorator(login_required, name='dispatch')
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'finance/invoice_list.html'
    context_object_name = 'invoices'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = Invoice.objects.select_related('reseller', 'transaction').order_by('-created_at')
        if hasattr(self.request.user, 'reseller_profile'):
            queryset = queryset.filter(reseller=self.request.user.reseller_profile)
        
        # Search
        query = self.request.GET.get('q')
        if query:
            if query.isdigit():
                 queryset = queryset.filter(id=query)
            else:
                 queryset = queryset.filter(reseller__name__icontains=query)
        
        # Filters
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Invoice.STATUS_CHOICES
        return context

@method_decorator(login_required, name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    fields = ['amount', 'method']
    template_name = 'finance/payment_form.html'
    success_url = reverse_lazy('invoice_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.invoice = self.invoice
        form.instance.reseller = self.invoice.reseller
        messages.success(self.request, "Payment recorded successfully.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        return context


@method_decorator(login_required, name='dispatch')
class InventoryListView(ListView):
    model = WarehouseStock
    template_name = 'inventory/list.html'
    context_object_name = 'stocks'
    paginate_by = 10

    def get_queryset(self):
        queryset = WarehouseStock.objects.select_related('warehouse', 'variant__product').order_by('warehouse', 'variant__product__name')
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(variant__product__name__icontains=query) | 
                Q(variant__sku__icontains=query) |
                Q(variant__color__icontains=query)
            )
            
        # Filters
        warehouse_id = self.request.GET.get('warehouse')
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
            
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(variant__product__category=category)
            
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(variant__product__brand=brand)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouses'] = Warehouse.objects.all()
        context['categories'] = Product.objects.values_list('category', flat=True).distinct().order_by('category')
        context['brands'] = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
        return context

@method_decorator(login_required, name='dispatch')
class StockInView(FormView):
    template_name = 'inventory/stock_in.html'
    form_class = StockAdjustmentForm
    success_url = '/inventory/'

    def form_valid(self, form):
        warehouse = form.cleaned_data['warehouse']
        variant = form.cleaned_data['variant']
        qty = form.cleaned_data['qty']
        
        try:
            with transaction.atomic():
                # 1. Update/Create Stock
                stock, created = WarehouseStock.objects.get_or_create(
                    warehouse=warehouse,
                    variant=variant
                )
                stock.qty_available += qty
                stock.save()

                # 2. Create Movement Log
                StockMovement.objects.create(
                    warehouse=warehouse,
                    variant=variant,
                    movement_type='IN',
                    qty=qty,
                    ref_type='ADJUST', # Or 'PURCHASE' if we had supplier module
                    ref_id=None,
                    user=self.request.user
                )
            messages.success(self.request, f"Successfully added {qty} {variant} to {warehouse}.")
        except Exception as e:
            messages.error(self.request, f"Error updating stock: {e}")
            return self.form_invalid(form)
            
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction/list.html'
    context_object_name = 'transactions'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = Transaction.objects.all().order_by('-created_at')
        if hasattr(self.request.user, 'reseller_profile'):
            queryset = queryset.filter(reseller=self.request.user.reseller_profile)
        
        # Search
        query = self.request.GET.get('q')
        if query:
             queryset = queryset.filter(
                Q(id__icontains=query) | 
                Q(reseller__name__icontains=query) |
                Q(warehouse__name__icontains=query)
            )
            
        # Filters
        warehouse_id = self.request.GET.get('warehouse')
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
            
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouses'] = Warehouse.objects.all()
        context['status_choices'] = Transaction.STATUS_CHOICES
        return context

@method_decorator(login_required, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = 'transaction/create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Check if user is a Reseller
        if hasattr(self.request.user, 'reseller_profile'):
            # Set the reseller field to the current user's profile and hide it
            reseller = self.request.user.reseller_profile
            form.fields['reseller'].initial = reseller
            form.fields['reseller'].widget = forms.HiddenInput()
            form.fields['reseller'].disabled = True # Ensure it can't be tampered easily, but need to handle save carefully
            # Actually if disabled, it might not send data. 
            # Better to just set initial and widget hidden, or handle in form_valid
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'DRAFT'
        
        # Enforce Reseller if user is one
        if hasattr(self.request.user, 'reseller_profile'):
            form.instance.reseller = self.request.user.reseller_profile
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('transaction_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class TransactionDetailView(DetailView, FormView):
    model = Transaction
    template_name = 'transaction/detail.html'
    context_object_name = 'transaction'
    form_class = TransactionDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = self.object.details.all()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if 'add_item' in request.POST:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'finalize' in request.POST:
            return self.finalize_transaction()
        
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        detail = form.save(commit=False)
        detail.transaction = self.object

        # Determine price: reseller-specific price if exists, otherwise variant default
        variant = detail.variant
        reseller = self.object.reseller
        reseller_price = None
        if reseller:
            reseller_price = ResellerPrice.objects.filter(reseller=reseller, variant=variant).first()

        if reseller_price:
            detail.price = reseller_price.custom_price
        else:
            detail.price = variant.default_price

        # Validate stock in the transaction's warehouse
        warehouse = self.object.warehouse
        stock = WarehouseStock.objects.filter(warehouse=warehouse, variant=variant).first()
        available = stock.qty_available if stock else 0

        if detail.qty > available:
            messages.error(self.request, f"Stok tidak cukup. Tersedia: {available}.")
            return redirect('transaction_detail', pk=self.object.pk)

        detail.save()
        messages.success(self.request, "Item added.")
        return redirect('transaction_detail', pk=self.object.pk)

    def finalize_transaction(self):
        try:
            # Trigger Signal
            self.object.status = 'FINAL'
            self.object.save()
            messages.success(self.request, "Transaction finalized successfully!")
            return redirect('transaction_list')
        except Exception as e:
            messages.error(self.request, f"Failed to finalize: {e}")
            # Reset status if save failed partially (though signal handles atomic usually, but pre_save validation might fail)
            self.object.refresh_from_db()
            return redirect('transaction_detail', pk=self.object.pk)

@method_decorator(login_required, name='dispatch')
class ReturnListView(ListView):
    model = ReturnHeader
    template_name = 'return/list.html'
    context_object_name = 'returns'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = ReturnHeader.objects.all().order_by('-created_at')
        if hasattr(self.request.user, 'reseller_profile'):
            queryset = queryset.filter(reseller=self.request.user.reseller_profile)
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(id__icontains=query) | 
                Q(reseller__name__icontains=query) |
                Q(invoice__id__icontains=query) |
                Q(details__variant__product__name__icontains=query) |
                Q(details__variant__sku__icontains=query)
            ).distinct()
            
        # Filters
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ReturnHeader.STATUS_CHOICES
        return context

@method_decorator(login_required, name='dispatch')
class ReturnCreateView(CreateView):
    model = ReturnHeader
    fields = ['reseller', 'warehouse', 'invoice']
    template_name = 'return/create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if hasattr(self.request.user, 'reseller_profile'):
            reseller = self.request.user.reseller_profile
            # Lock Reseller Field
            form.fields['reseller'].initial = reseller
            form.fields['reseller'].widget = forms.HiddenInput()
            form.fields['reseller'].disabled = True
            
            # Filter Invoices to only own invoices
            form.fields['invoice'].queryset = Invoice.objects.filter(reseller=reseller)
        return form

    def form_valid(self, form):
        if hasattr(self.request.user, 'reseller_profile'):
            form.instance.reseller = self.request.user.reseller_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('return_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ReturnDetailView(DetailView):
    model = ReturnHeader
    template_name = 'return/detail.html'
    context_object_name = 'return_header'

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'reseller_profile'):
            queryset = queryset.filter(reseller=self.request.user.reseller_profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter variants only from the invoice
        invoice = self.object.invoice
        transaction_details = invoice.transaction.details.all()
        
        allowed_variants = []
        for td in transaction_details:
            # Calculate already returned in OTHER returns
            already_returned_others = ReturnDetail.objects.filter(
                return_header__invoice=invoice,
                variant=td.variant
            ).exclude(return_header=self.object).aggregate(total=Sum('qty'))['total'] or 0
            
            # Count what's already in THIS return
            in_this_return = ReturnDetail.objects.filter(
                return_header=self.object,
                variant=td.variant
            ).aggregate(total=Sum('qty'))['total'] or 0
            
            remaining = td.qty - already_returned_others - in_this_return
            if remaining > 0:
                allowed_variants.append({
                    'id': td.variant.id,
                    'name': td.variant.product.name,
                    'sku': td.variant.sku,
                    'max_qty': remaining
                })
        
        context['allowed_variants'] = allowed_variants
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.status == 'FINAL':
            messages.error(request, "Retur yang sudah final tidak bisa diubah.")
            return redirect('return_detail', pk=self.object.pk)

        if 'finalize' in request.POST:
            try:
                self.object.status = 'FINAL'
                self.object.save()
                messages.success(request, "Retur berhasil difinalisasi.")
            except Exception as e:
                messages.error(request, f"Gagal finalisasi: {e}")
            return redirect('return_detail', pk=self.object.pk)
        
        if 'remove_item' in request.POST:
            detail_id = request.POST.get('detail_id')
            ReturnDetail.objects.filter(id=detail_id, return_header=self.object).delete()
            messages.success(request, "Item dihapus.")
            return redirect('return_detail', pk=self.object.pk)
        
        # Add Item Logic
        variant_id = request.POST.get('variant')
        try:
            qty = int(request.POST.get('qty', 0))
        except ValueError:
            qty = 0
        
        if variant_id and qty > 0:
            invoice = self.object.invoice
            # 1. Check if variant is in the original transaction
            td = TransactionDetail.objects.filter(transaction=invoice.transaction, variant_id=variant_id).first()
            if not td:
                messages.error(request, "Produk tidak ada dalam invoice ini.")
                return redirect('return_detail', pk=self.object.pk)
            
            # 2. Calculate sisa yang bisa di-retur
            total_returned_others = ReturnDetail.objects.filter(
                return_header__invoice=invoice,
                variant_id=variant_id
            ).exclude(return_header=self.object).aggregate(total=Sum('qty'))['total'] or 0
            
            current_detail = ReturnDetail.objects.filter(return_header=self.object, variant_id=variant_id).first()
            current_qty = current_detail.qty if current_detail else 0
            
            if (total_returned_others + current_qty + qty) > td.qty:
                sisa = td.qty - total_returned_others - current_qty
                messages.error(request, f"Total retur melebihi qty invoice ({td.qty}). Sisa yang bisa di-retur: {sisa}")
                return redirect('return_detail', pk=self.object.pk)

            if current_detail:
                current_detail.qty += qty
                current_detail.save()
            else:
                ReturnDetail.objects.create(
                    return_header=self.object,
                    variant_id=variant_id,
                    qty=qty
                )
            messages.success(request, "Item retur ditambahkan.")
        
        return redirect('return_detail', pk=self.object.pk)
