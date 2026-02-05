from django import forms
from .models import Warehouse, Variant, StockMovement, Transaction, TransactionDetail, Payment

class StockAdjustmentForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label="Select Warehouse")
    variant = forms.ModelChoiceField(queryset=Variant.objects.all(), empty_label="Select Product Variant")
    qty = forms.IntegerField(min_value=1, label="Quantity", widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered h-24', 'rows': 3}), required=False)

    class Meta:
        model = StockMovement
        fields = ['warehouse', 'variant', 'qty']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'variant': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def save(self, user=None, commit=True):
        # We don't save StockMovement directly via form save because we need custom logic
        # But for ModelForm compliance we can use it to clean data
        return super().save(commit=False)

class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['reseller', 'warehouse']
        widgets = {
            'reseller': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'warehouse': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = ['variant', 'qty', 'price']
        widgets = {
            'variant': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'qty': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }

