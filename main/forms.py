from django import forms


class AddToCartForm(forms.Form):
    # 取り出しの際にnumが辞書型のキーなり、入力された数値が値となる
    num = forms.IntegerField(
        label='数量',
        min_value=1,
        required=True
    )


class PurchaseForm(forms.Form):
    zip_code = forms.CharField(
        label='郵便番号',
        max_length=7,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '数字7桁（ハイフンなし）'}
        )
    )

    address = forms.CharField(
        label='住所', max_length=100, required=False
    )


class TestForm(forms.Form):
    test = forms.CharField()
