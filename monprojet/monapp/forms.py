from django import forms
from .models import Product, ProductAttribute, ProductItem, ProductAttributeValue

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm): 
    class Meta:
        model = Product
        #fields = '__all__'
        exclude = ('price_ttc', 'status')

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['name']

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ['product', 'attributes', 'code']

class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = ['value', 'product_attribute', 'position']