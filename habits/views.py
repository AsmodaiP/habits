from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from .models import Habit
import datetime as dt
from datetime import timedelta


from .forms import HabitForm, CheckForm


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


def get_checks_for_habit_by_period(habit, **kwargs):
    repeat = habit.repeat
    if repeat == 'D':
        day = kwargs.get('day')
        return get_days_checks(habit, day)
    if repeat == 'W':
        week = kwargs.get('week')
        year = kwargs.get('year')
        return get_week_checks(habit, week, year)
    if repeat == 'M':
        year = kwargs.get('year')
        month = kwargs.get('month')
        return get_month_checks(habit, month, year)


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


def get_previous_week_with_year(weekNum, year):
    weekNum -= 1
    if weekNum == 0:
        year -= 1
        weekNum = dt.datetime(year, 12, 31).isocalendar()[1]
    return weekNum, year


def get_previous_month_with_year(month, year):
    month -= 1
    if month == 0:
        year -= 1
        month = 12
    return month, year
def check_today_is_accomplished(habit):
    checks = get_days_checks(habit, dt.datetime.today())
    if get_count_required_sum(checks, habit)>0:
        return True
    return False

def get_streak_of_habit(habit):
    checks = habit.checks.all()
    if len(checks) == 0:
        return 0
    last = checks.first()
    habit_streak = 0
    repeat = habit.repeat
    last_date = last.date
    current_day = dt.date.today()
    current_year, current_weekNum, current_DOW = current_day.isocalendar()
    current_month = dt.datetime.today().month
    if repeat == 'D':
        day = dt.date.today()
        while True:
            days_checks = get_days_checks(habit, day)
            if len(days_checks) == 0 and day != current_day:
                return habit_streak
            if habit.is_quantity is False:
                if len(days_checks) != 0:
                    habit_streak += 1
            else:
                if not check_sum_of_day(days_checks, habit.quantity):
                    return habit_streak
                habit_streak += 1
            day -= timedelta(days=1)
    if repeat == 'W':
        year, weekNum, DOW = last_date.isocalendar()
        while True:
            week_checks = get_week_checks(habit, weekNum, year)
            if len(week_checks) == 0 and (
                    current_weekNum != weekNum and current_year != year):
                return habit_streak
            weakly_streak = get_count_required_sum(week_checks, habit)
            if check_required_repeats(weakly_streak, habit) or (
                    current_weekNum == weekNum and current_year == year):
                habit_streak += get_count_required_sum(week_checks, habit)
            else:
                return habit_streak
            weekNum, year = get_previous_week_with_year(weekNum, year)
    if repeat == 'M':
        year = last.date.year
        month = last.date.month
        month_streak = 0
        while True:
            month_checks = get_month_checks(habit, month, year)
            if len(month_checks) == 0 and (
                    month != current_month and year != current_year):
                return habit_streak
            month_streak += get_count_required_sum(month_checks, habit)
            if check_required_repeats(month_streak, habit):
                habit_streak += get_count_required_sum(month_checks, habit)
            else:
                return habit_streak
            month, year = get_previous_month_with_year(month, year)


def get_list_user_habist(request):
    if request.user.is_authenticated:
        return list(Habit.objects.filter(author=request.user))
    else:
        return []


def get_habits_for_context(habits):
    habits_for_context = []
    for habit in habits:
        streak = get_streak_of_habit(habit)
        habit_info = {
            'name': habit.title,
            'streak': streak,
            'form': CheckForm(initial={'habit': habit}),
            'today_is_accomplished': check_today_is_accomplished(habit)
        }
        habits_for_context.append(habit_info)
    return habits_for_context


def list_of_habits(request):
    habits = get_list_user_habist(request)
    form = CheckForm(request.POST or None)
    habits_for_context = get_habits_for_context(habits)
    context = {
        'form': form,
        'habits': habits_for_context
        }
    return render(request, 'habits/list_of_habits.html', context)


def checking(request):
    form = CheckForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('list_of_habits')
