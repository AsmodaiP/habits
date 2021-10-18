from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Habit(models.Model):
    CHOICES = (
        ('D', 'daily'),
        ('W', 'Weakly'),
        ('M', 'Mounthly'),
    )
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Название'
    )
    created = models.DateField(auto_now_add=True, editable=True)
    is_quantity = models.BooleanField(
        default=False,
        verbose_name='Количественная'
        )
    quantity = models.FloatField(default=0)
    repeat = models.CharField(
        max_length=1,
        choices=CHOICES,
        default=CHOICES[0][0],
        verbose_name='Период повторения'
    )
    times_in_period = models.IntegerField(
        max_length=2,
        default=1,
        verbose_name='Количетсво повторений в период'
        )

    class HabitPriority(models.IntegerChoices):
        LOW = 0, 'Low'
        NORMAL = 1, 'Normal'
        HIGH = 2, 'High'

    priority = models.IntegerField(
        default=HabitPriority.LOW,
        choices=HabitPriority.choices,
        verbose_name='Приоритет'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-priority',)
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class Check(models.Model):
    date = models.DateField(auto_now_add=True)
    quantity = models.FloatField(default=0, verbose_name='Количество')
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='checks',
        verbose_name='Привычка'
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Отметка'
        verbose_name_plural = 'Отметки'

    def __str__(self) -> str:
        return f'Отметка привычки {self.habit} от {self.date}'
