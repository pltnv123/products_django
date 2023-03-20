from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins

class CustomSignupForm(SignupForm):

    # переопределение группы
    # def save(self, request):
    #     user = super().save(request)
    #     common_users = Group.objects.get(name="common users")
    #     user.groups.add(common_users)
    #     return user

    # #сообщение просто текст
    # def save(self, request):
    #     user = super().save(request)
    #     print(user)
    #     send_mail(
    #         subject='Добро пожаловать в наш интернет-магазин!',
    #         message=f'{user.username}, вы успешно зарегистрировались!',
    #         from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
    #         recipient_list=[user.email],
    #     )
    #     return user

    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    first_name = forms.CharField(label="Ваше имя")
    last_name = forms.CharField(label="Ваша фамилия")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повторите пароль")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )