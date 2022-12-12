from django.urls import path
from store_main import views

app_name = 'store_main'
urlpatterns = [
    path('store_index/', views.store_index, name='store_index'),
    path('product_new/', views.product_new, name='product_new'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_edit/<int:product_id>', views.product_edit,
         name='product_edit'),
    path('product_csv/', views.product_csv, name='product_csv'),
    path('test_index/', views.test_index, name='test_index'),
]
