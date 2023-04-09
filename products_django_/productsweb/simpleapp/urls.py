from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, multiply, ProductCreate, ProductUpdate, ProductDelete, subscriptions, IndexView
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', ProductsList.as_view(), name='product_list'),    # FIXME

   path('index/', IndexView.as_view(), name='index'),        # TODO use async

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', cache_page(60*10)(ProductDetail.as_view()), name='product_detail'), # добавим кэширование на детали товара. Раз в 10 минут товар
                                                                                        # будет записываться в кэш для экономии ресурсов.
   path('multiply/', multiply),

   # path('create/', create_product, name='product_create') ==
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]