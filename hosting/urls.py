from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:pk>', views.HostingUpdate.as_view(), name = 'hosting_edit'),
    path('create', views.HostingCreate.as_view(), name = 'hosting_create'),
    path('', views.hosting, name = 'hosting_list'),
    path('delete/<int:pk>', views.HostingDelete.as_view(), name = 'hosting_delete'),
]