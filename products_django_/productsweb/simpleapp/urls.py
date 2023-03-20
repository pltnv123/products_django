from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, multiply, ProductCreate, ProductUpdate, ProductDelete, subscriptions, IndexView


urlpatterns = [

   path('', ProductsList.as_view(), name='product_list'),

   path('index/', IndexView.as_view(), name='index'),

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
   path('multiply/', multiply),

   # path('create/', create_product, name='product_create') ==
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]