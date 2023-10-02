from django.urls import path
from django.conf.urls import url
from .views import new_personal, view_personal, ajax_del_personal

urlpatterns = [
	path('view_personal', view_personal, name = 'view_personal'),
	path('new_personal', new_personal, name = 'new_personal'),
]

urlpatterns += [
	path('ajax/del-personal/', ajax_del_personal, name = 'ajax_del_personal'),

]
