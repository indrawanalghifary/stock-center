from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from .models import WarehouseStock, StockMovement, Variant, Warehouse, Transaction, TransactionDetail, Invoice, Payment
from .forms import StockAdjustmentForm, TransactionCreateForm, TransactionDetailForm

@login_required
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    # Dashboard Stats
    total_stock_value = 0 # Need calculation logic if variant has cost, currently using default_price as estimate
    # Simple count for now
    stock_count = WarehouseStock.objects.aggregate(total=Sum('qty_available'))['total'] or 0
    
    total_receivables = Invoice.objects.filter(status__in=['UNPAID', 'PARTIAL']).aggregate(
        total=Sum('total_amount'), 
        paid=Sum('paid_amount')
    )
    receivables_value = (total_receivables['total'] or 0) - (total_receivables['paid'] or 0)
    
    transaction_count = Transaction.objects.filter(created_at__date=timezone.now().date()).count()

    context = {
        'stock_count': stock_count,
        'receivables_value': receivables_value,
        'transaction_count': transaction_count,
    }
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

    def get_queryset(self):
        return Invoice.objects.select_related('reseller', 'transaction').order_by('-created_at')

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

    def get_queryset(self):
        return WarehouseStock.objects.select_related('warehouse', 'variant__product').order_by('warehouse', 'variant__product__name')

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

@method_decorator(login_required, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = 'transaction/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'DRAFT'
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