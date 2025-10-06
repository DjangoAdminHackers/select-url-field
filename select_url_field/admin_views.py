import json
from importlib import import_module

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse


@staff_member_required
def select_url_choices(request):
    mod_path, func_name = settings.SELECT_URL_CHOICES_FUNC.rsplit(".", 1)
    mod = import_module(mod_path)
    choices_func = getattr(mod, func_name)
    choices = []
    try:
        choices_data = choices_func()
        for item in choices_data:
            choice_group = {
                "group_name": item[0],
                "group_choices": [[x[1], x[0]] for x in item[1]],
            }
            choices.append(choice_group)
    except (ValueError, IndexError, TypeError):
        pass

    return HttpResponse(json.dumps(choices), content_type="application/json")
