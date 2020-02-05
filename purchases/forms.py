from django import forms

from .models import Vendor

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