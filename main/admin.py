from django.contrib import admin
# from main.models import Product, Sale
#
# from import_export import resources
# from main.models import Product
# from import_export.admin import ImportMixin
#
# from import_export.formats import base_formats
#
#
# # csvのインポートエクスポート
# class ProductResource(resources.ModelResource):
#
#     class Meta:
#         # 対象モデル
#         model = Product
#         # オブジェクト識別の要素
#         import_id_fields = ('code',)
#
#
# class ProductAdmin(ImportMixin, admin.ModelAdmin):
#     list_display = ('name', 'description', 'price', 'amount', 'image', 'code',)
#     resource_class = ProductResource
#     formats = [base_formats.CSV]
#
#
# # モデルのadmin表示
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Sale)
