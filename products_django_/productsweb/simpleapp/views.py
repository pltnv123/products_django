from datetime import datetime

from django.core.cache import cache
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Product, Subscription, Category, Author
from .filters import ProductFilter
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .tasks import hello, printer
from django.contrib.auth.models import Group
from django.db.models import Sum
import logging
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.utils import timezone

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


# logger = logging.getLogger('productsweb')


def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)


class ProductsList(ListView):
    # logger.info('Product list view accessed')
    model = Product
    ordering = 'name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)

        # Возвращаем из функции отфильтрованный список товаров
        # свойство qs преобразовывает объект класса в QuerySet
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class ProductCreate(PermissionRequiredMixin, CreateView):
    # logger.info('DEBUG')

    permission_required = ('simpleapp.add_product',)
    raise_exception = True
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.quantity = 13
        return super().form_valid(form)


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


# функция создает продукт  == class ProductCreate(CreateView):
    # def create_product(request):
    #     if request.method == 'POST':
    #         form = ProductForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect('/products/')
    #
    #     form = ProductForm()
    #     return render(request, 'product_edit.html', {'form': form})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()
    # Вывод запроса из БД
    print(Category.objects.all().query)

    """Это список всех категорий, объекты данного списка имеют атрибут user_subcribed, который возвращает True если
     текущий пользователь подписан и False если нет."""

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')


@login_required()
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='newuser')

    if not user.groups.filter(name='newuser').exists():
        group.user_set.add(user)
        Author.objects.create(authorUser=user)
    return redirect('product_list')


class Index2(View):
    """ Просто выводит одну строку и переводит на другой язык (gettext - "_") """

    def get(self, request):
        curent_time = timezone.now()
        string = _('Hello world')

        models = Product.objects.all()

        context = {
            'string': string,
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones,  # добавляем в контекст все доступные часовые пояса

        }

        return HttpResponse(render(request, 'index2.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META.get('HTTP_REFERER'))
