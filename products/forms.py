from django import forms
from .models import Product
from .widgets import JSONEditorWidget

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'specifications': JSONEditorWidget(attrs={'cols': 80, 'rows': 20}),
        }
