import datetime

from django.contrib.auth import get_user_model
from django.db import models

from .validators import date_validator

User = get_user_model()

CHOICES = (
    ('D', 'daily'),
    ('W', 'Weakly'),
    ('M', 'Mounthly'),
    )


class HabitPriority(models.IntegerChoices):
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'


class Habit(models.Model):

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
        default=1,
        verbose_name='Количетсво повторений в период'
        )

    priority = models.IntegerField(
        default=HabitPriority.LOW,
        choices=HabitPriority.choices,
        verbose_name='Приоритет'
    )

    best_streak = models.IntegerField(
        default=0,
        verbose_name='Лучший стрик'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-priority',)
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique habit for author'
            ),
        )


class Check(models.Model):
    date = models.DateField(default=datetime.date.today,validators=(date_validator,))
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
