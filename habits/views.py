from django.db.models.aggregates import Sum
from django.shortcuts import render
from .models import Habit
from datetime import timedelta


def check_sum_of_day(days_checks, quantity):
    sum = days_checks.aggregate(Sum('quantity'))['quantity__sum']
    return sum >= quantity


def get_year_checks(habit, year):
    return habit.checks.filter(date__year=year)


def get_month_checks(habit, month, year):
    return habit.checks.filter(date__month=month, date__year=year)


def get_days_checks(habit, day):
    return habit.checks.filter(date=day)


def get_streak_of_habit(habit):
    checks = habit.checks.all()
    if len(checks) == 0:
        return 0
    last = checks.first()
    habit_streak = 0
    repeat = habit.repeat
    last_date = last.date
    if repeat == 'D':
        while True:
            days_checks = get_days_checks(habit, last_date)
            last_date -= timedelta(days=1)
            if len(days_checks) == 0:
                return habit_streak
            if habit.is_quantity is False:
                habit_streak += 1
            else:
                if check_sum_of_day(days_checks, habit.quantity):
                    habit_streak += 1

    if repeat == 'M':
        year = last.date.year
        month = last.date.month
        while True:
            month_checks = get_month_checks(habit, month, year)
            if len(month_checks) == 0:
                return habit_streak
            month -= 1
            if month == 0:
                year -= 1
                month = 12
            sum_of_days = month_checks.values(
                'date').annotate(sum=Sum('quantity'))
            if habit.is_quantity is False:
                habit_streak += len(sum_of_days)
            else:
                for sum in sum_of_days:
                    if sum['sum'] >= habit.quantity:
                        habit_streak += 1


def list_of_habits(request):
    if request.user.is_authenticated:
        habits = list(Habit.objects.filter(author=request.user))
    else:
        habits = []
    habit_info = {}
    habits_for_context = {}
    habits_items = {}
    for habit in habits:
        streak = get_streak_of_habit(habit)
        habit_info = {
            'name': habit.title,
            'streak': streak
        }
        habits_items[habit.id] = habit_info
        habits_for_context = {'habits': habits_items}
    return render(request, 'habits/list_of_habits.html',
                  {'habits': habits_for_context})
