from django import forms

from .models import Vendor, Purchase

class VendorForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    class Meta:
        model=Vendor
        exclude = [
            'created', 'updated', 'created_by',
            'updated_by'
        ]
        widget={'description': forms.TextInput()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class PurchaseForm(forms.ModelForm):
    date_purchase = forms.DateInput()
    date_invoice = forms.DateInput()

    class Meta:
        model=Purchase
        fields=['vendor','date_purchase','observations',
            'invoice_number','date_invoice','sub_total',
            'discount','total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['date_purchase'].widget.attrs['readonly'] = True
        self.fields['date_invoice'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['discount'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True