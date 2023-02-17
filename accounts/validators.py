from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template.context_processors import request
from django.utils.translation import gettext_lazy as _


def validate_zetech_email(value):
    if not value.endswith('@zetech.ac.ke'):
        messages.error(request, f'Only emails with the domain "@zetech.ac.ke" are allowed.')
