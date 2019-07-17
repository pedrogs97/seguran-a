import django_tables2 as tables
from .models import Hosting

class HostingTable(tables.Table):
    class Meta:
        model = Hosting
        template_name = 'django_tables2/bootstrap.html'