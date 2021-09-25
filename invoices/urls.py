from django.urls import path
from django.conf.urls import url
from .views import new_invoice, view_invoice, ajax_del_invoice

urlpatterns = [
	path('view_invoice', view_invoice, name = 'view_invoice'),
	path('new_invoice', new_invoice, name = 'new_invoice'),
]

urlpatterns += [
	path('ajax/del-invoice/', ajax_del_invoice, name = 'ajax_del_invoice'),

]