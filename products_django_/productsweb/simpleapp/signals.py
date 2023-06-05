from django.db.models.signals import post_save

from django.contrib.auth.models import User, Group

from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Product


# @receiver(post_save, sender=Product)
# def product_created(instance, **kwargs):
#     print('Создан товар', instance)

@receiver(post_save, sender=Product)
def product_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Новый товар в категории {instance.category}'

    text_content = (
        f'Товар: {instance.name}\n'
        f'Цена: {instance.price}\n\n'
        f'Ссылка на товар: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Товар: {instance.name}<br>'
        f'Цена: {instance.price}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на товар</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])            # Титл сооб / текст сооб / from_email - с какого эмейла / [кому]
        msg.attach_alternative(html_content, "text/html")
        msg.send()

## еще пример отправки
# def send_message():
#     email = "test@example.com"
#     subject = "Subject"
#
#     text_content = "Hello"
#     html_content = "<b>Hello</b>"
#
#     msg = EmailMultiAlternatives(subject, text_content, None, [email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='newuser')
        instance.groups.add(group)