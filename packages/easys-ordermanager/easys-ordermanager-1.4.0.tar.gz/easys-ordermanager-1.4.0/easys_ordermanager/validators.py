import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


def comma_separated_period_validatior(val):
    values = val.split(',')
    if len(values) != 2:
        raise ValidationError('', 'invalid')
    if values[0].isdigit() and values[1].isdigit():
        return val
    raise ValidationError('', 'invalid')


class DomainNameValidator(RegexValidator):
    message = _('Enter a valid plain or internationalized domain name value')
    regex = re.compile((
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    ), re.IGNORECASE)

    def __init__(self, accept_idna=True, **kwargs):
        message = kwargs.get('message')
        self.accept_idna = accept_idna
        super(DomainNameValidator, self).__init__(**kwargs)
        if not self.accept_idna and message is None:
            self.message = _('Enter a valid domain name value')

    def __call__(self, value):
        try:
            super(DomainNameValidator, self).__call__(value)
        except ValidationError as exc:
            if not self.accept_idna:
                raise
            if not value:
                raise
            try:
                idnavalue = value.encode('idna')
            except UnicodeError:
                raise exc
            super(DomainNameValidator, self).__call__(idnavalue)


class HexColorValidator(RegexValidator):
    regex = re.compile(r'^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$')
    message = _('Enter a valid hex color (starting with a "#" sign)')
