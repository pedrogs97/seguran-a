import django_tables2 as tables
from .models import Hosting

class HostingTable(tables.Table):
    class Meta:
        model = Hosting
        template_name = 'django_tables2/bootstrap.html'



class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name

class SimpleTable(tables.Table):
    selection = CheckBoxColumnWithName(verbose_name="Remover", accessor="pk")
    # selection = tables.CheckBoxColumn(attrs={"th_input":"teste"}, accessor="pk")
    class Meta:
        model = Hosting
        template_name = 'django_tables2/bootstrap.html'