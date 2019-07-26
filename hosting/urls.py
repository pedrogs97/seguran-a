from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:pk>', views.HostingUpdate.as_view(), name = 'hosting_edit'),
    path('create', views.HostingCreate.as_view(), name = 'hosting_create'),
    path('SENAI', views.HostingList.as_view(), name = 'hosting_list'),
    path('SENAI/tabela-preco', views.tabelaPrecos, name = 'tabela_preco'),
    path('', views.redirectSenai, name = 'redirect'),
    path('delete/<int:pk>', views.HostingDelete.as_view(), name = 'hosting_delete'),
    path('FIEB/', views.hostingFieb, name = 'hosting_fieb'),
    path('serv-add/delete/<int:pk>', views.Servicos_adicionaisDelete.as_view(), name='servicos_delete'),
    path('serv-add/edit/<int:pk>', views.Servicos_adicionaisUpdate.as_view(), name='servicos_edit'),
    path('serv-add/create', views.Sevicos_adicionaisCreate.as_view(), name='servicos_adicionais'),
    path('backup-add/delete/<int:pk>', views.Backup_dadosDelete.as_view(), name='backup_delete'),
    path('backup-add/edit/<int:pk>', views.Backup_dadosUpdate.as_view(), name='backup_edit'),
    path('backup-add/create', views.Backup_dadosCreate.as_view(), name='backup_adicionais'),
]