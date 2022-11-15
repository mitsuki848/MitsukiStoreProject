from django import forms
from store_main.models import Product, ImageZip


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'amount', 'image', 'code',)


class CsvUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')


class ImageZipForm(forms.ModelForm):
    class Meta:
        model = ImageZip
        fields = ('zip_import',)
