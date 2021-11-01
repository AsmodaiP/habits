from django.core.exceptions import ValidationError
from django.utils.timezone import now


def date_validator(value):
    if value > now():
        raise ValidationError(
            f'Не корректное значение поля date: {value}!')