from django.urls import path
from django.conf.urls import url
from .views import new_protocol, view_protocol, ajax_del_protocol

urlpatterns = [
	path('view_protocol', view_protocol, name = 'view_protocol'),
	path('new_protocol', new_protocol, name = 'new_protocol'),
]

urlpatterns += [
	path('ajax/del-protocol/', ajax_del_protocol, name = 'ajax_del_protocol'),

]