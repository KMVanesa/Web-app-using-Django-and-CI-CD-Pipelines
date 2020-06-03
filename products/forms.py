from django import forms
from products.models import Products


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductForm(forms.ModelForm):
    class Meta():
        model = Products
        labels = {
            "isbn": "ISBN"
        }
        fields = ('isbn', 'title', 'authors', 'publication_date', 'quantity', 'price')
        widgets = {
            'publication_date': DateInput()
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta():
        model = Products
        labels = {
            "isbn": "ISBN"
        }
        fields = ('isbn', 'title', 'authors', 'publication_date', 'quantity', 'price')
        widgets = {
            'publication_date': DateInput()
        }
