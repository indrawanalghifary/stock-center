from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Warehouse, Variant, StockMovement, Transaction, TransactionDetail, Payment, Reseller, Product, ResellerPrice

class PlainCheckboxInput(forms.CheckboxInput):
    """Custom CheckboxInput yang render input checkbox polos tanpa wrapper"""
    def render(self, name, value, attrs=None, renderer=None):
        # Build attributes
        if attrs is None:
            attrs = {}
        
        attrs['type'] = 'checkbox'
        attrs['name'] = name
        
        # Add id if not present
        if 'id' not in attrs and name:
            attrs['id'] = f'id_{name}'
        
        # Handle checked state
        if value:
            attrs['checked'] = True
        
        # Build HTML
        html = f'<input'
        for key, val in attrs.items():
            if key == 'checked' and val is True:
                html += f' {key}'
            elif key == 'checked':
                continue
            elif val is True:
                html += f' {key}'
            elif val is False:
                continue
            else:
                html += f' {key}="{val}"'
        
        html += '>'
        return mark_safe(html)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}), required=False, help_text="Kosongkan jika tidak ingin mengubah password (untuk edit).")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'is_staff': PlainCheckboxInput(),
            'is_active': PlainCheckboxInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

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
            'is_active': PlainCheckboxInput(),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'category': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'brand': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'is_active': PlainCheckboxInput(),
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

