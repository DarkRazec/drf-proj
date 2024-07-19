from rest_framework.exceptions import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in dict(value).get(self.field):
            raise ValidationError('Неверный адрес')
