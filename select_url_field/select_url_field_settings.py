from django.conf import settings

URL_CHOICES_FUNC = getattr(settings, 'SELECT_URL_CHOICES_FUNC', 'choices_func.get_url_choices')