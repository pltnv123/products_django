# Generated by Django 4.1.7 on 2023-04-30 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simpleapp', '0004_alter_product_price_alter_product_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(help_text='Имя категории', max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(help_text='Имя категории', max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en_us',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Имя категории', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='This is the help text'),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratingAuthor', models.SmallIntegerField(default=0)),
                ('authorUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
