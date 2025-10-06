from django.urls import re_path
from select_url_field.admin_views import select_url_choices

urlpatterns = [
    re_path(
        r"^$",
        select_url_choices,
        name="select_url_choices",
    ),
]
