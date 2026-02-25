from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q, F, Count
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import WarehouseStock, StockMovement, Variant, Warehouse, Transaction, TransactionDetail, Invoice, Payment, ReturnHeader, ReturnDetail, Product, ResellerPrice, Reseller, PackingTask, PackingItem
from .forms import UserForm, StockAdjustmentForm, TransactionCreateForm, TransactionDetailForm, PaymentForm, ResellerForm, ProductForm, VariantForm, ResellerPriceForm, WarehouseForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Admins').exists()

@login_required
def master_data_dashboard(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Admins').exists()):
        messages.error(request, "Anda tidak memiliki akses ke Master Data.")
        return redirect('home')
    return render(request, 'master/dashboard.html')

@method_decorator(login_required, name='dispatch')
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'master/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) | Q(email__icontains=query) |
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('user_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah User / Pegawai"
        return context

@method_decorator(login_required, name='dispatch')
class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('user_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit User / Pegawai"
        return context

@method_decorator(login_required, name='dispatch')
class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('user_list')

@method_decorator(login_required, name='dispatch')
class ResellerListView(AdminRequiredMixin, ListView):
    model = Reseller
    template_name = 'master/reseller_list.html'
    context_object_name = 'resellers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Reseller.objects.all().order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class ResellerDetailView(AdminRequiredMixin, DetailView):
    model = Reseller
    template_name = 'master/reseller_detail.html'
    context_object_name = 'reseller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special_prices'] = self.object.special_prices.select_related('variant__product')
        context['invoices'] = Invoice.objects.filter(reseller=self.object).order_by('-created_at')[:5]
        return context

@method_decorator(login_required, name='dispatch')
class ResellerCreateView(AdminRequiredMixin, CreateView):
    model = Reseller
    form_class = ResellerForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('reseller_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah Reseller"
        return context

@method_decorator(login_required, name='dispatch')
class ResellerUpdateView(AdminRequiredMixin, UpdateView):
    model = Reseller
    form_class = ResellerForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('reseller_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Reseller"
        return context

@method_decorator(login_required, name='dispatch')
class ResellerDeleteView(AdminRequiredMixin, DeleteView):
    model = Reseller
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('reseller_list')

@method_decorator(login_required, name='dispatch')
class WarehouseListView(AdminRequiredMixin, ListView):
    model = Warehouse
    template_name = 'master/warehouse_list.html'
    context_object_name = 'warehouses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Warehouse.objects.all().order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(location__icontains=query)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class WarehouseCreateView(AdminRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('warehouse_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah Gudang"
        return context

@method_decorator(login_required, name='dispatch')
class WarehouseUpdateView(AdminRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('warehouse_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Gudang"
        return context

@method_decorator(login_required, name='dispatch')
class WarehouseDeleteView(AdminRequiredMixin, DeleteView):
    model = Warehouse
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('warehouse_list')

@method_decorator(login_required, name='dispatch')
class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'master/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all().order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(category__icontains=query) | Q(brand__icontains=query)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class ProductDetailView(AdminRequiredMixin, DetailView):
    model = Product
    template_name = 'master/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = self.object.variants.all()
        return context

@method_decorator(login_required, name='dispatch')
class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('product_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah Produk"
        return context

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('product_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Produk"
        return context

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('product_list')

@method_decorator(login_required, name='dispatch')
class VariantCreateView(AdminRequiredMixin, CreateView):
    model = Variant
    form_class = VariantForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('product_list')
    
    def get_initial(self):
        initial = super().get_initial()
        product_id = self.request.GET.get('product')
        if product_id:
            initial['product'] = product_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah Varian"
        return context

@method_decorator(login_required, name='dispatch')
class VariantUpdateView(AdminRequiredMixin, UpdateView):
    model = Variant
    form_class = VariantForm
    template_name = 'master/form.html'
    success_url = reverse_lazy('product_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Varian"
        return context

@method_decorator(login_required, name='dispatch')
class VariantDeleteView(AdminRequiredMixin, DeleteView):
    model = Variant
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('product_list')

@method_decorator(login_required, name='dispatch')
class ResellerPriceListView(AdminRequiredMixin, ListView):
    model = ResellerPrice
    template_name = 'master/reseller_price_list.html'
    context_object_name = 'special_prices'
    paginate_by = 10

    def get_queryset(self):
        queryset = ResellerPrice.objects.select_related('reseller', 'variant__product').order_by('reseller__name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(reseller__name__icontains=query) | 
                Q(variant__sku__icontains=query) |
                Q(variant__product__name__icontains=query)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class ResellerPriceCreateView(AdminRequiredMixin, CreateView):
    model = ResellerPrice
    form_class = ResellerPriceForm
    template_name = 'master/reseller_price_form.html'
    success_url = reverse_lazy('reseller_price_list')

    def get_initial(self):
        initial = super().get_initial()
        reseller_id = self.request.GET.get('reseller')
        if reseller_id:
            initial['reseller'] = reseller_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tambah Harga Khusus"
        return context

@method_decorator(login_required, name='dispatch')
class ResellerPriceUpdateView(AdminRequiredMixin, UpdateView):
    model = ResellerPrice
    form_class = ResellerPriceForm
    template_name = 'master/reseller_price_form.html'
    success_url = reverse_lazy('reseller_price_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Harga Khusus"
        return context

@method_decorator(login_required, name='dispatch')
class ResellerPriceDeleteView(AdminRequiredMixin, DeleteView):
    model = ResellerPrice
    template_name = 'master/confirm_delete.html'
    success_url = reverse_lazy('reseller_price_list')

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
                 queryset = queryset.filter(Q(id=query) | Q(reseller__name__icontains=query))
            else:
                 queryset = queryset.filter(reseller__name__icontains=query)
        
        # Filter Reseller
        reseller_id = self.request.GET.get('reseller_id')
        if reseller_id:
            queryset = queryset.filter(reseller_id=reseller_id)
        
        # Filter Status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter Date Range
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
        context['resellers'] = Reseller.objects.all().order_by('name')
        
        # Calculate total for filtered invoices
        queryset = self.get_queryset()
        total_amount = queryset.aggregate(total=Sum('total_amount'))['total'] or 0
        paid_amount = queryset.aggregate(total=Sum('paid_amount'))['total'] or 0
        remaining = total_amount - paid_amount
        
        context['total_amount'] = total_amount
        context['paid_amount'] = paid_amount
        context['remaining_balance'] = remaining
        context['invoice_count'] = queryset.count()
        context['selected_reseller'] = self.request.GET.get('reseller_id')
        context['selected_status'] = self.request.GET.get('status')
        context['selected_start_date'] = self.request.GET.get('start_date')
        context['selected_end_date'] = self.request.GET.get('end_date')
        
        return context

@method_decorator(login_required, name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
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
    paginate_by = 100

    def get_queryset(self):
        queryset = WarehouseStock.objects.select_related('warehouse', 'variant__product')
        
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
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'warehouse')
        sort_order = self.request.GET.get('order', 'asc')
        
        sort_fields = {
            'warehouse': 'warehouse__name',
            'product': 'variant__product__name',
            'sku': 'variant__sku',
            'variant': 'variant__color',
            'stock': 'qty_available',
        }
        
        order_field = sort_fields.get(sort_by, 'warehouse__name')
        if sort_order == 'desc':
            order_field = f'-{order_field}'
        
        queryset = queryset.order_by(order_field)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Hitung Total Nominal dan Total Qty untuk SELURUH hasil filter (bukan cuma yang di halaman ini)
        from django.db.models import F, Sum, DecimalField
        filtered_qs = self.get_queryset()
        total_nominal = filtered_qs.aggregate(
            total=Sum(F('qty_available') * F('variant__default_price'), output_field=DecimalField())
        )['total'] or 0
        
        total_qty = filtered_qs.aggregate(
            total=Sum('qty_available')
        )['total'] or 0
        
        # 2. Tambahkan nominal_value ke objek yang sedang ditampilkan di HALAMAN ini saja
        # context['stocks'] adalah daftar objek yang sudah dipaginasi
        for s in context['stocks']:
            s.nominal_value = s.qty_available * s.variant.default_price
            
        context['total_nominal'] = total_nominal
        context['total_qty'] = total_qty
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
class TransactionDetailUpdateView(UpdateView):
    """Edit TransactionDetail item"""
    model = TransactionDetail
    template_name = 'transaction/detail_form.html'
    fields = ['qty']
    
    def get_object(self, queryset=None):
        return get_object_or_404(TransactionDetail, pk=self.kwargs['detail_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction'] = self.object.transaction
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        transaction = self.object.transaction
        
        # Hanya bisa edit jika status DRAFT
        if transaction.status != 'DRAFT':
            messages.error(request, "Hanya bisa edit item pada transaksi DRAFT.")
            return redirect('transaction_detail', pk=transaction.pk)
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        old_qty = self.object.qty
        new_qty = form.cleaned_data['qty']
        
        # Validate stock if qty increased
        if new_qty > old_qty:
            qty_increase = new_qty - old_qty
            warehouse = self.object.transaction.warehouse
            variant = self.object.variant
            stock = WarehouseStock.objects.filter(warehouse=warehouse, variant=variant).first()
            available = stock.qty_available if stock else 0
            
            if qty_increase > available:
                messages.error(self.request, f"Stok tidak cukup untuk penambahan. Tersedia: {available}.")
                return redirect('transaction_detail', pk=self.object.transaction.pk)
        
        self.object = form.save()
        messages.success(self.request, "Item berhasil diupdate.")
        return redirect('transaction_detail', pk=self.object.transaction.pk)
    
    def get_success_url(self):
        return reverse('transaction_detail', kwargs={'pk': self.object.transaction.pk})

@method_decorator(login_required, name='dispatch')
class TransactionDetailDeleteView(DeleteView):
    """Delete TransactionDetail item"""
    model = TransactionDetail
    template_name = 'transaction/detail_confirm_delete.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(TransactionDetail, pk=self.kwargs['detail_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction'] = self.object.transaction
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        transaction = self.object.transaction
        
        # Hanya bisa delete jika status DRAFT
        if transaction.status != 'DRAFT':
            messages.error(request, "Hanya bisa hapus item pada transaksi DRAFT.")
            return redirect('transaction_detail', pk=transaction.pk)
        
        # Confirm delete
        if 'confirm' in request.POST:
            messages.success(request, "Item berhasil dihapus.")
            transaction_pk = transaction.pk
            self.object.delete()
            return redirect('transaction_detail', pk=transaction_pk)
        else:
            return redirect('transaction_detail', pk=transaction.pk)
    
    def get_success_url(self):
        return reverse('transaction_detail', kwargs={'pk': self.object.transaction.pk})

@method_decorator(login_required, name='dispatch')
class TransactionDeleteView(DeleteView):
    """Delete Transaction (only if DRAFT)"""
    model = Transaction
    template_name = 'transaction/confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Hanya bisa delete jika status DRAFT
        if self.object.status != 'DRAFT':
            messages.error(request, "Hanya bisa hapus transaksi dengan status DRAFT.")
            return redirect('transaction_detail', pk=self.object.pk)
        
        # Confirm delete
        if 'confirm' in request.POST:
            messages.success(request, "Transaksi berhasil dihapus.")
            self.object.delete()
            return redirect('transaction_list')
        else:
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

@method_decorator(login_required, name='dispatch')
class PackingListView(ListView):
    model = PackingTask
    template_name = 'packing/list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = PackingTask.objects.select_related('user', 'warehouse').prefetch_related('items__variant__product').order_by('-created_at')
        
        # Admin can see all, regular user might only see their own packing tasks
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name='Admins').exists():
             # If you want to restrict to only their own tasks:
             # queryset = queryset.filter(user=self.request.user)
             pass

        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user__username__icontains=query) | 
                Q(warehouse__name__icontains=query)
            )
            
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
            
        return queryset

@method_decorator(login_required, name='dispatch')
class AnalyticsView(ListView):
    template_name = 'analytics.html'
    context_object_name = 'movements'
    model = StockMovement

    def get_queryset(self):
        queryset = StockMovement.objects.select_related('variant__product', 'warehouse').order_by('-created_at')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        if not start_date and not end_date:
            # Default to current month if no range provided
            from datetime import datetime
            now = timezone.now()
            month_start = datetime(now.year, now.month, 1, 0, 0, 0)
            if now.month == 12:
                month_end = datetime(now.year + 1, 1, 1, 0, 0, 0)
            else:
                month_end = datetime(now.year, now.month + 1, 1, 0, 0, 0)
            queryset = queryset.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Base query for analytics in the selected range
        base_trx_query = TransactionDetail.objects.filter(transaction__status='FINAL')
        base_movement_query = StockMovement.objects.all()

        if start_date:
            base_trx_query = base_trx_query.filter(transaction__created_at__date__gte=start_date)
            base_movement_query = base_movement_query.filter(created_at__date__gte=start_date)
        if end_date:
            base_trx_query = base_trx_query.filter(transaction__created_at__date__lte=end_date)
            base_movement_query = base_movement_query.filter(created_at__date__lte=end_date)

        if not start_date and not end_date:
            # Default to current month using datetime range
            from datetime import datetime
            month_start = datetime(now.year, now.month, 1, 0, 0, 0)
            if now.month == 12:
                month_end = datetime(now.year + 1, 1, 1, 0, 0, 0)
            else:
                month_end = datetime(now.year, now.month + 1, 1, 0, 0, 0)
            base_trx_query = base_trx_query.filter(
                transaction__created_at__gte=month_start,
                transaction__created_at__lt=month_end
            )
            base_movement_query = base_movement_query.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            )

        is_reseller = hasattr(self.request.user, 'reseller_profile')
        reseller = self.request.user.reseller_profile if is_reseller else None

        if is_reseller:
            base_trx_query = base_trx_query.filter(transaction__reseller=reseller)

        # 1. Group by Product (Top Products) - Top 10 SKUs
        total_period_sales = base_trx_query.aggregate(total=Sum('subtotal'))['total'] or 0
        product_grouping = base_trx_query.values(
            'variant__product__name', 'variant__sku'
        ).annotate(
            total_qty=Sum('qty'),
            total_value=Sum('subtotal')
        ).order_by('-total_qty')[:10]

        # 2. Group by Reseller (Leaderboard - available to all)
        reseller_grouping = base_trx_query.values(
            'transaction__reseller__id',
            'transaction__reseller__name'
        ).annotate(
            total_qty=Sum('qty'),
            total_value=Sum('subtotal')
        ).order_by('-total_value')

        top_reseller_name = "-"
        if reseller_grouping.exists():
            top_reseller_name = reseller_grouping[0]['transaction__reseller__name']

        # 2b. Top Category (Admins only)
        top_category_name = "-"
        if not is_reseller:
            category_grouping = base_trx_query.values(
                'variant__product__category'
            ).annotate(
                total_qty=Sum('qty')
            ).order_by('-total_qty')
            if category_grouping.exists():
                top_category_name = category_grouping[0]['variant__product__category']

        # 2c. Return Rate (Admins only)
        return_rate = 0
        if not is_reseller:
            total_out = base_trx_query.aggregate(total=Sum('qty'))['total'] or 0

            # Base return query
            base_return_query = ReturnDetail.objects.filter(return_header__status='FINAL')
            if start_date:
                base_return_query = base_return_query.filter(return_header__created_at__date__gte=start_date)
            if end_date:
                base_return_query = base_return_query.filter(return_header__created_at__date__lte=end_date)
            if not start_date and not end_date:
                # Use datetime range instead of __year/__month
                from datetime import datetime
                month_start = datetime(now.year, now.month, 1, 0, 0, 0)
                if now.month == 12:
                    month_end = datetime(now.year + 1, 1, 1, 0, 0, 0)
                else:
                    month_end = datetime(now.year, now.month + 1, 1, 0, 0, 0)
                base_return_query = base_return_query.filter(
                    return_header__created_at__gte=month_start,
                    return_header__created_at__lt=month_end
                )

            total_ret = base_return_query.aggregate(total=Sum('qty'))['total'] or 0
            if total_out > 0:
                return_rate = (total_ret / total_out) * 100

        # 3. Stock Movement Statistics by Type (IN, OUT, RETURN) - Admins only
        stock_movement_stats = []
        if not is_reseller:
            movement_summary = base_movement_query.values('movement_type').annotate(
                total_qty=Sum('qty'),
                total_nominal=Sum(F('qty') * F('variant__default_price'))
            ).order_by('movement_type')
            stock_movement_stats = list(movement_summary)

        # 4. Top 10 Resellers by Debt (current_balance) - Admins only
        top_reseller_debts = []
        if not is_reseller:
            top_reseller_debts = list(Reseller.objects.filter(
                current_balance__gt=0
            ).order_by('-current_balance')[:10].values('id', 'name', 'current_balance'))

        # 5. Reseller Pickup Ranking (by quantity and nominal) - Admins only
        reseller_pickup_ranking = []
        if not is_reseller:
            reseller_pickup_ranking = list(base_trx_query.values(
                'transaction__reseller__id',
                'transaction__reseller__name'
            ).annotate(
                pickup_qty=Sum('qty'),
                pickup_nominal=Sum('subtotal')
            ).order_by('-pickup_qty')[:10])

        # Movement summary for template (backward compatibility)
        movement_summary = []
        if not is_reseller:
            movement_summary = base_movement_query.values('movement_type').annotate(total_qty=Sum('qty'))

        # 4. Dynamic Sales Trend based on filter
        sales_trend = []
        import datetime
        
        if start_date and end_date:
            # Daily Trend for the selected range
            s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            # Limit to 60 days to prevent chart clutter, otherwise maybe group by week?
            # For now, let's just do daily.
            delta = e_date - s_date

            curr = s_date
            while curr <= e_date:
                daily_sales_query = TransactionDetail.objects.filter(
                    transaction__status='FINAL',
                    transaction__created_at__date=curr
                )
                if is_reseller:
                    daily_sales_query = daily_sales_query.filter(transaction__reseller=reseller)

                total_val = daily_sales_query.aggregate(total=Sum('subtotal'))['total'] or 0
                sales_trend.append({
                    'label': curr.strftime('%d %b'),
                    'value': float(total_val)
                })
                curr += datetime.timedelta(days=1)

                # Safety break if range is too long (e.g. > 90 days)
                if len(sales_trend) > 90:
                    break
        else:
            # Default: Last 6 Months (Monthly)
            for i in range(5, -1, -1):
                # Calculate month start and end
                target_date = now.replace(day=1) - datetime.timedelta(days=i*30)
                target_date = target_date.replace(day=1)
                t_year, t_month = target_date.year, target_date.month

                # Use datetime range instead of __year/__month
                month_start = datetime.datetime(t_year, t_month, 1, 0, 0, 0)
                if t_month == 12:
                    month_end = datetime.datetime(t_year + 1, 1, 1, 0, 0, 0)
                else:
                    month_end = datetime.datetime(t_year, t_month + 1, 1, 0, 0, 0)

                monthly_sales_query = TransactionDetail.objects.filter(
                    transaction__status='FINAL',
                    transaction__created_at__gte=month_start,
                    transaction__created_at__lt=month_end
                )
                if is_reseller:
                    monthly_sales_query = monthly_sales_query.filter(transaction__reseller=reseller)

                total_val = monthly_sales_query.aggregate(total=Sum('subtotal'))['total'] or 0
                sales_trend.append({
                    'label': target_date.strftime('%b %Y'),
                    'value': float(total_val)
                })

        context.update({
            'start_date': start_date,
            'end_date': end_date,
            'total_period_sales': total_period_sales,
            'product_grouping': product_grouping,
            'reseller_grouping': reseller_grouping,
            'top_reseller_name': top_reseller_name,
            'top_category_name': top_category_name,
            'return_rate': return_rate,
            'movement_summary': movement_summary,
            'stock_movement_stats': stock_movement_stats,
            'top_reseller_debts': top_reseller_debts,
            'reseller_pickup_ranking': reseller_pickup_ranking,
            'sales_trend': sales_trend,
            'is_reseller': is_reseller,
        })
        return context

@method_decorator(login_required, name='dispatch')
class ResellerSkuAnalysisView(ListView):
    """View for analyzing SKU pickup by each reseller with date filtering"""
    template_name = 'analysis/reseller_sku_analysis.html'
    context_object_name = 'reseller_sku_data'
    model = TransactionDetail

    def get_queryset(self):
        queryset = TransactionDetail.objects.filter(
            transaction__status='FINAL'
        ).select_related(
            'variant__product', 'transaction__reseller', 'transaction__warehouse'
        ).order_by('-transaction__created_at')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        reseller_id = self.request.GET.get('reseller_id')

        if start_date:
            queryset = queryset.filter(transaction__created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction__created_at__date__lte=end_date)

        if not start_date and not end_date:
            # Default: show current month data
            # Use timezone-aware datetime for compatibility with MySQL timezone settings
            from datetime import datetime
            now = timezone.now()
            month_start = datetime(now.year, now.month, 1, 0, 0, 0)
            if now.month == 12:
                month_end = datetime(now.year + 1, 1, 1, 0, 0, 0)
            else:
                month_end = datetime(now.year, now.month + 1, 1, 0, 0, 0)

            # Filter using date range - Django will handle timezone conversion
            queryset = queryset.filter(
                transaction__created_at__gte=month_start,
                transaction__created_at__lt=month_end
            )

        if reseller_id:
            queryset = queryset.filter(transaction__reseller_id=reseller_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        reseller_id = self.request.GET.get('reseller_id')

        # Base query
        base_query = TransactionDetail.objects.filter(transaction__status='FINAL')

        if start_date:
            base_query = base_query.filter(transaction__created_at__date__gte=start_date)
        if end_date:
            base_query = base_query.filter(transaction__created_at__date__lte=end_date)

        if not start_date and not end_date:
            # Default: show current month data
            from datetime import datetime
            month_start = datetime(now.year, now.month, 1, 0, 0, 0)
            if now.month == 12:
                month_end = datetime(now.year + 1, 1, 1, 0, 0, 0)
            else:
                month_end = datetime(now.year, now.month + 1, 1, 0, 0, 0)

            base_query = base_query.filter(
                transaction__created_at__gte=month_start,
                transaction__created_at__lt=month_end
            )

        if reseller_id:
            base_query = base_query.filter(transaction__reseller_id=reseller_id)

        # All resellers for filter dropdown
        resellers = Reseller.objects.all().order_by('name')

        # Summary: Total SKU taken by each reseller
        reseller_summary = base_query.values(
            'transaction__reseller__id',
            'transaction__reseller__name'
        ).annotate(
            total_qty=Sum('qty'),
            total_nominal=Sum('subtotal'),
            total_skus=Sum('qty', distinct=True)
        ).order_by('-total_qty')

        # Top 10 SKUs overall
        top_skus = base_query.values(
            'variant__id',
            'variant__sku',
            'variant__product__name',
            'variant__product__category',
            'variant__color',
            'variant__size'
        ).annotate(
            total_qty=Sum('qty'),
            total_nominal=Sum('subtotal'),
            reseller_count=Count('transaction__reseller', distinct=True)
        ).order_by('-total_qty')[:10]

        # SKU by Reseller breakdown (for the main table)
        sku_by_reseller = base_query.values(
            'transaction__reseller__id',
            'transaction__reseller__name',
            'variant__id',
            'variant__sku',
            'variant__product__name'
        ).annotate(
            total_qty=Sum('qty'),
            total_nominal=Sum('subtotal'),
            avg_price=Sum('subtotal') / Sum('qty')
        ).order_by('transaction__reseller__name', '-total_qty')

        # Calculate totals
        total_qty = base_query.aggregate(total=Sum('qty'))['total'] or 0
        total_nominal = base_query.aggregate(total=Sum('subtotal'))['total'] or 0

        context.update({
            'start_date': start_date,
            'end_date': end_date,
            'selected_reseller_id': reseller_id,
            'resellers': resellers,
            'reseller_summary': reseller_summary,
            'top_skus': top_skus,
            'sku_by_reseller': sku_by_reseller,
            'total_qty': total_qty,
            'total_nominal': total_nominal,
        })
        return context

@login_required
def scanner(request):
    return render(request, 'scanner.html')

@login_required
def scanner_advanced(request):
    warehouses = Warehouse.objects.filter(is_active=True)
    resellers = Reseller.objects.all()
    
    is_reseller = hasattr(request.user, 'reseller_profile')
    user_reseller = request.user.reseller_profile if is_reseller else None

    context = {
        'warehouses': warehouses,
        'resellers': resellers,
        'is_reseller': is_reseller,
        'user_reseller': user_reseller,
    }
    return render(request, 'scanner_advanced.html', context)

@login_required
@require_POST
def process_scanned_data(request):
    try:
        data = json.loads(request.body)
        mode = data.get('mode') # PACKING, STOCK, ORDER
        warehouse_id = data.get('warehouse_id')
        reseller_id = data.get('reseller_id')
        items = data.get('items', []) # List of {sku: ..., qty: ...}

        if not items:
            return JsonResponse({'success': False, 'error': 'Tidak ada item untuk diproses'})

        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        unknown_skus = []
        processed_count = 0
        
        if mode == 'STOCK':
            with transaction.atomic():
                for item in items:
                    variant = Variant.objects.filter(sku=item['sku']).first()
                    if not variant:
                         unknown_skus.append(item['sku'])
                         continue
                    
                    qty = int(item['qty'])
                    stock, created = WarehouseStock.objects.get_or_create(
                        warehouse=warehouse,
                        variant=variant
                    )
                    stock.qty_available += qty 
                    stock.save()

                    StockMovement.objects.create(
                        warehouse=warehouse,
                        variant=variant,
                        movement_type='IN',
                        qty=qty,
                        ref_type='SCAN_OPNAME',
                        user=request.user
                    )
                    processed_count += 1
            
            if processed_count == 0:
                return JsonResponse({'success': False, 'error': f'Tidak ada SKU yang valid. SKU tidak dikenal: {", ".join(unknown_skus)}'})

            msg = f'Berhasil update stok {processed_count} item.'
            if unknown_skus:
                msg += f' SKU tidak dikenal: {", ".join(unknown_skus)}'
            return JsonResponse({'success': True, 'message': msg})

        elif mode == 'ORDER':
            if not reseller_id:
                return JsonResponse({'success': False, 'error': 'Reseller harus dipilih untuk mode Pesanan'})
            
            reseller = get_object_or_404(Reseller, id=reseller_id)
            
            with transaction.atomic():
                trx = Transaction.objects.create(
                    reseller=reseller,
                    warehouse=warehouse,
                    user=request.user,
                    status='DRAFT'
                )
                
                for item in items:
                    variant = Variant.objects.filter(sku=item['sku']).first()
                    if not variant:
                        unknown_skus.append(item['sku'])
                        continue
                    
                    qty = int(item['qty'])
                    reseller_price = ResellerPrice.objects.filter(reseller=reseller, variant=variant).first()
                    price = reseller_price.custom_price if reseller_price else variant.default_price
                    
                    TransactionDetail.objects.create(
                        transaction=trx,
                        variant=variant,
                        qty=qty,
                        price=price
                    )
                    processed_count += 1
            
            if processed_count == 0:
                return JsonResponse({'success': False, 'error': f'Tidak ada SKU yang valid. SKU tidak dikenal: {", ".join(unknown_skus)}'})

            msg = f'Berhasil membuat Pesanan TRX-{trx.id} dengan {processed_count} item.'
            if unknown_skus:
                msg += f' SKU tidak dikenal: {", ".join(unknown_skus)}'
            
            return JsonResponse({
                'success': True, 
                'message': msg, 
                'url': reverse('transaction_detail', kwargs={'pk': trx.pk})
            })

        elif mode == 'PACKING':
            with transaction.atomic():
                packing_fee_per_item = 500 # Bisa dipindahkan ke settings atau config
                total_qty = sum(int(item['qty']) for item in items)
                
                task = PackingTask.objects.create(
                    user=request.user,
                    warehouse=warehouse,
                    total_items=total_qty,
                    packing_fee_per_item=packing_fee_per_item,
                    total_fee=total_qty * packing_fee_per_item
                )

                for item in items:
                    variant = Variant.objects.filter(sku=item['sku']).first()
                    if not variant:
                        unknown_skus.append(item['sku'])
                        continue
                    
                    qty = int(item['qty'])
                    PackingItem.objects.create(
                        packing_task=task,
                        variant=variant,
                        qty=qty
                    )
                    processed_count += 1
            
            if processed_count == 0:
                return JsonResponse({'success': False, 'error': f'Tidak ada SKU yang valid. SKU tidak dikenal: {", ".join(unknown_skus)}'})

            msg = f'Berhasil menyimpan data Packing (ID: {task.id}). Total Item: {total_qty}. Biaya: Rp {task.total_fee}'
            if unknown_skus:
                msg += f' SKU tidak dikenal: {", ".join(unknown_skus)}'
            
            return JsonResponse({'success': True, 'message': msg})

        return JsonResponse({'success': False, 'error': 'Mode tidak valid'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def variant_barcode(request, pk):
    variant = get_object_or_404(Variant, pk=pk)
    return render(request, 'inventory/barcode_page.html', {'variant': variant})

@login_required
def bulk_barcode(request):
    variant_ids = request.GET.getlist('variants')
    
    # List to store duplicated variants
    labels = []
    
    for v_id in variant_ids:
        variant = get_object_or_404(Variant, id=v_id)
        # Get qty from query param qty_ID, default to 1
        qty_param = request.GET.get(f'qty_{v_id}', 1)
        try:
            qty = int(qty_param)
        except ValueError:
            qty = 1
            
        # Add the variant to our labels list multiple times
        for i in range(qty):
            labels.append({
                'id': f"{variant.id}_{i}", # Unique ID for JS selector
                'sku': variant.sku
            })
    
    return render(request, 'inventory/bulk_barcode.html', {'labels': labels})

@login_required
def invoice_qrcode(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'finance/qrcode_page.html', {'invoice': invoice})

@login_required
def scan_lookup(request):
    code = request.GET.get('code', '')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    # Check for Invoice ID (format: INV-123)
    if code.startswith('INV-'):
        try:
            inv_id = int(code.replace('INV-', ''))
            invoice = Invoice.objects.get(id=inv_id)
            # Redirect to transaction detail which is effectively the invoice detail
            return JsonResponse({'url': reverse('transaction_detail', kwargs={'pk': invoice.transaction.pk})})
        except (ValueError, Invoice.DoesNotExist):
            pass

    # Try SKU lookup
    variant = Variant.objects.filter(sku=code).first()
    if variant:
        return JsonResponse({'url': reverse('variant_detail', kwargs={'pk': variant.pk})})

    return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)

@method_decorator(login_required, name='dispatch')
class VariantDetailView(DetailView):
    model = Variant
    template_name = 'inventory/variant_detail.html'
    context_object_name = 'variant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocks'] = WarehouseStock.objects.filter(variant=self.object).select_related('warehouse')
        
        # Add reseller price if user is a reseller
        if hasattr(self.request.user, 'reseller_profile'):
            reseller = self.request.user.reseller_profile
            special_price = ResellerPrice.objects.filter(reseller=reseller, variant=self.object).first()
            if special_price:
                context['reseller_price'] = special_price.custom_price
                
        return context

@login_required
def api_variant_detail(request, variant_id):
    """API endpoint to get variant details including default price"""
    try:
        variant = Variant.objects.get(id=variant_id)
        return JsonResponse({
            'id': variant.id,
            'sku': variant.sku,
            'default_price': float(variant.default_price),
            'product': variant.product.name,
        })
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)