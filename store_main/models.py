from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    """商品"""
    name = models.CharField(verbose_name='商品名', max_length=128)
    description = models.TextField(verbose_name='商品説明', max_length=5000,
                                   blank=True, default='')
    price = models.PositiveIntegerField(verbose_name='価格', blank=True,
                                        default=0)
    amount = models.PositiveIntegerField(verbose_name='在庫数', blank=True,
                                         default=0)
    image = models.ImageField(verbose_name='商品画像', upload_to='product', )
    code = models.CharField(verbose_name='商品コード', max_length=128, )

    # adminでの表示名
    def __str__(self):
        return self.name


class Sale(models.Model):
    """売上情報"""
    # https://itc.tokyo/django/foreignkey/
    # Productモデルと多対一の関係を作る
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='商品名', )
    # https://qiita.com/Quest_love33/items/77c5cbf3acd2c09edd0a
    # 使用しているUserモデルと多対一の関係を作る
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name='ユーザー名', )
    amount = models.PositiveIntegerField(verbose_name="購入個数", default=0)
    price = models.PositiveIntegerField(verbose_name='商品単価', default=0)
    total_price = models.PositiveIntegerField(verbose_name='小計', default=0)
    zip_code = models.CharField(verbose_name='郵便番号', max_length=128,
                                blank=True, default='')
    address = models.CharField(verbose_name='住所', max_length=128, blank=True,
                               default='')
    created_at = models.DateTimeField(verbose_name='販売日', auto_now=True)


class ImageZip(models.Model):
    """
    zipファイル受け入れ用モデル
    https://stackoverflow.com/questions/37234473/django-admin-images-in-zip-file-and-inserting-each-image-info-in-a-database
    """
    zip_import = models.FileField(blank=True, upload_to='image_zip',
                                  help_text='※画像のzipファイルをアップロードしてください。')
