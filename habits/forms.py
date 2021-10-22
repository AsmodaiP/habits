from django import forms

from .models import Habit, Check


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('quantity', 'habit')
        verbose_name = 'Отметки'
        verbose_name_plural = 'Отметки'
        widgets = {'habit_title': forms.HiddenInput()}


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = '__all__'
