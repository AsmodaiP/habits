from django.db.models.aggregates import Sum
from django.shortcuts import render
from .models import Habit
import datetime as dt
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


def get_week_checks(habit, week, year):
    return habit.checks.filter(date__week=week, date__year=year)


def get_count_required_sum(checks, habit):
    habit_streak = 0
    sum_of_days = checks.values('date').annotate(sum=Sum('quantity'))
    if habit.is_quantity is False:
        return len(sum_of_days)
    for sum in sum_of_days:
        if sum['sum'] >= habit.quantity:
            habit_streak += 1
    return habit_streak


def check_required_repeats(streak_of_perion, habit):
    return streak_of_perion >= habit.times_in_period


def get_streak_of_habit(habit):
    checks = habit.checks.all()
    if len(checks) == 0:
        return 0
    last = checks.first()
    habit_streak = 0
    repeat = habit.repeat
    last_date = last.date
    last_year, last_weekNum, last_DOW = last_date.isocalendar()
    current_year, current_weekNum, current_DOW = dt.date.today().isocalendar()
    current_month = dt.datetime.today().month
    if repeat == 'D':
        current_day = dt.date.today()
        while True:
            days_checks = get_days_checks(habit, current_day)
            if len(days_checks) == 0 and current_day != dt.date.today():
                return habit_streak
            current_day -= timedelta(days=1)
            if habit.is_quantity is False:
                habit_streak += 1
            else:
                if not check_sum_of_day(days_checks, habit.quantity):
                    return habit_streak
                habit_streak += 1
    if repeat == 'W':
        while True:
            week_checks = get_week_checks(habit, last_weekNum, last_year)
            if len(week_checks) == 0 and (current_weekNum != last_weekNum and current_year != last_year):
                return habit_streak
            last_weekNum -= 1
            if last_weekNum == 0:
                last_year -= 1
                last_weekNum = dt.datetime(last_year, 12, 31).isocalendar()[1]
            weakly_streak = get_count_required_sum(week_checks, habit)
            if check_required_repeats(weakly_streak, habit):
                habit_streak += get_count_required_sum(week_checks, habit)
            else:
                return habit_streak
    if repeat == 'M':
        year = last.date.year
        month = last.date.month
        month_streak = 0
        while True:
            month_checks = get_month_checks(habit, month, year)
            if len(month_checks) == 0 and (month != current_month and year != current_year):
                return habit_streak
            month -= 1
            if month == 0:
                year -= 1
                month = 12
            month_streak += get_count_required_sum(month_checks, habit)
            if check_required_repeats(month_streak, habit):
                habit_streak += get_count_required_sum(month_checks, habit)
            else:
                return habit_streak


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
