from django import forms  

from .models import Category, SubCategory, Brand, UnitOfMeasurement, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'status']
        labels = {'description': 'Category description', 
                  'status': 'Status'}
        widget = {'description': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SubCategoryForm(forms.ModelForm):

    # FILTER CATEGORY TO SHOW ONLY ACTIVES CATEGORY ON THE FORM
    category = forms.ModelChoiceField(
        queryset = Category.objects.filter(status=True).order_by('description')
    )

    class Meta:
        model = SubCategory
        fields = ['category','description', 'status']
        labels = {'description': 'SubCategory description', 
                  'status': 'Status'}
        widget = {'description': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['category'].empty_label = "Select category"


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'status']
        labels = {'description': 'Brand description', 
                  'status': 'Status'}
        widget = {'description': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class UnitOfMeasurementForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasurement
        fields = ['description', 'status']
        labels = {'description': 'Unit description', 
                  'status': 'Status'}
        widget = {'description': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'cod','barcode','description', 'status', 
            'price', 'stock', 'last_purchase', 
            'brand', 'subcategory', 'unit_measurements'
        ]
        exclude = [
            'created', 'updated', 'created_by',
            'updated_by'
        ]
        widget = {'description': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['last_purchase'].widget.attrs['readonly'] = True
        self.fields['stock'].widget.attrs['readonly'] = True