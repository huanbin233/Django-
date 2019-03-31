import django_tables2 as tables
from .models import Notify_h
class PersonTable(tables.Table):
    class Meta:
        model = Notify_h
        template_name = "django_tables2/semantic.html"