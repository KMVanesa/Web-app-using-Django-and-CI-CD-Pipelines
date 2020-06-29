from django import forms
from products.models import Products, BookImage


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


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = BookImage
        fields = ('image',)


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
