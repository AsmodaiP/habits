# Generated by Django 3.2.7 on 2021-10-18 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habits', '0006_auto_20211011_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='check',
            options={'ordering': ('-date',), 'verbose_name': 'Отметка', 'verbose_name_plural': 'Отметки'},
        ),
        migrations.RemoveField(
            model_name='habit',
            name='times_in_perion',
        ),
        migrations.AddField(
            model_name='habit',
            name='times_in_period',
            field=models.IntegerField(default=1, max_length=2, verbose_name='Количетсво повторений в период'),
        ),
        migrations.AlterField(
            model_name='check',
            name='habit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='habits.habit', verbose_name='Привычка'),
        ),
        migrations.AlterField(
            model_name='check',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='is_quantity',
            field=models.BooleanField(default=False, verbose_name='Количественная'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High')], default=0, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='repeat',
            field=models.CharField(choices=[('D', 'daily'), ('W', 'Weakly'), ('M', 'Mounthly')], default='D', max_length=1, verbose_name='Период повторения'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]