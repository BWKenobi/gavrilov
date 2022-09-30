from django.urls import path
from django.conf.urls import url
from .views import new_statement, view_statement, ajax_del_statement

urlpatterns = [
	path('view_statement', view_statement, name = 'view_statement'),
	path('new_statement', new_statement, name = 'new_statement'),
]

urlpatterns += [
	path('ajax/del-statement/', ajax_del_statement, name = 'ajax_del_statement'),

]