from django.core.exceptions import ValidationError
from datetime import datetime


class CustomValidators:
    @staticmethod
    def validate_non_negative(value):
        if value < 0:
            raise ValidationError('Value must not be negative number.')
    
    @staticmethod
    def validate_positive(value):
        if value <= 0:
            raise ValidationError('Value must be positive number.')

    @staticmethod
    def validate_no_special_characters(value):
        if not value.isalnum():
            raise ValidationError('Text should contain only alphanumeric characters.')

    @staticmethod
    def validate_future_date(value):
        if value < datetime.date.today():
            raise ValidationError('Date cannot be in the past.')
        
    @staticmethod
    def validate_past(value):
        if value > datetime.date.today():
            raise ValidationError('Date cannot be in the future.')
