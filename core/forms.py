from django import forms
from .models import Warehouse, Variant, StockMovement, Transaction, TransactionDetail, Payment, Reseller, Product, ResellerPrice

class StockAdjustmentForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label="Select Warehouse", widget=forms.Select(attrs={'class': 'select searchable-select w-full'}))
    variant = forms.ModelChoiceField(queryset=Variant.objects.all(), empty_label="Select Product Variant", widget=forms.Select(attrs={'class': 'select searchable-select w-full'}))
    qty = forms.IntegerField(min_value=1, label="Quantity", widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered h-24', 'rows': 3}), required=False)

    class Meta:
        model = StockMovement
        fields = ['warehouse', 'variant', 'qty']

class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['reseller', 'warehouse']
        widgets = {
            'reseller': forms.Select(attrs={'class': 'select searchable-select w-full'}),
            'warehouse': forms.Select(attrs={'class': 'select searchable-select w-full'}),
        }

class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = ['variant', 'qty']
        widgets = {
            'variant': forms.Select(attrs={'class': 'select searchable-select w-full'}),
            'qty': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': 1}),
        }

class PaymentForm(forms.ModelForm):
    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Transfer', 'Transfer'),
        ('E-Wallet', 'E-Wallet'),
        ('Lainnya', 'Lainnya'),
    ]
    
    method = forms.ChoiceField(
        choices=METHOD_CHOICES, 
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'step': '0.01'})
    )

    class Meta:
        model = Payment
        fields = ['amount', 'method']

class ResellerForm(forms.ModelForm):
    class Meta:
        model = Reseller
        fields = ['name', 'phone', 'address', 'credit_limit', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'credit_limit': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'user': forms.Select(attrs={'class': 'select searchable-select w-full'}),
        }

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'location': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'category': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'brand': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['product', 'sku', 'color', 'size', 'default_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'select searchable-select w-full'}),
            'sku': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'color': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'size': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'default_price': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }

class ResellerPriceForm(forms.ModelForm):
    class Meta:
        model = ResellerPrice
        fields = ['reseller', 'variant', 'custom_price']
        widgets = {
            'reseller': forms.Select(attrs={'class': 'select searchable-select w-full'}),
            'variant': forms.Select(attrs={'class': 'select searchable-select w-full'}),
            'custom_price': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }

