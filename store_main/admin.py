from django.contrib import admin
from store_main.models import Product, Sale, ImageZip

from import_export import resources
from import_export.admin import ImportMixin

from import_export.formats import base_formats


class ProductResource(resources.ModelResource):
    """
    csvのインポートエクスポート
    https://tech.fragment.co.jp/python/django/django-import-export/
    """

    class Meta:
        # 対象モデル
        model = Product
        # オブジェクト識別の要素
        import_id_fields = ('code',)


class ProductAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'amount', 'image', 'code',)
    resource_class = ProductResource
    formats = [base_formats.CSV]


# モデルのadmin表示
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale)
admin.site.register(ImageZip)
