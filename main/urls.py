from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('test_index/', views.test_index, name='test_index'),
    path('', views.index, name='index'),
    path('product_detail/<int:product_id>/', views.product_detail,
         name='product_detail'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('change_product_amount/', views.change_product_amount, name='change_product_amount'),
    path('order_history/', views.order_history, name='order_history'),
    # 決済
    path('payment/', views.payment, name="payment"),
    path('thanks/', views.thanks, name="thanks"),
]
