import functools
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "To hasło jest zbyt krótkie. Hasło musi zawierać co najmniej %(min_length)d znaków.",
                    "To hasło jest zbyt krótkie. Hasło musi zawierać co najmniej %(min_length)d znaków.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Hasło powinno zawierać co najmniej %(min_length)d znaków.",
            "Hasło powinno zawierać co najmniej %(min_length)d znaków.",
            self.min_length
        ) % {'min_length': self.min_length}

class UserAttributeSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    if verbose_name == 'imię':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do imienia."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    elif verbose_name == 'nazwisko':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do nazwiska."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    elif verbose_name == 'adres e-mail':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do adresu e-mail."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    elif verbose_name == 'nazwa użytkownika':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do nazwy użytkownika."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )

    def get_help_text(self):
        return _('Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych.')


class CommonPasswordValidator:
    """
    Validate whether the password is a common password.

    The password is rejected if it occurs in a provided list of passwords,
    which may be gzipped. The list Django ships with contains 20000 common
    passwords (lowercased and deduplicated), created by Royce Williams:
    https://gist.github.com/roycewilliams/281ce539915a947a23db17137d91aeb7
    The password list must be lowercased to match the comparison in validate().
    """
    DEFAULT_PASSWORD_LIST_PATH = Path(__file__).resolve().parent / 'common-passwords.txt.gz'

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path, 'rt', encoding='utf-8') as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("To hasło jest zbyt powszechne."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _('Twoje hasło nie może być powszechnie używanym hasłem.')


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("To hasło jest w całości numeryczne."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('Twoje hasło nie może być w całości numeryczne.')
