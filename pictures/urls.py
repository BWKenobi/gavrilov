from django.urls import path
from django.conf.urls import url
from .views import load_image, edit_image, ajax_del_image

urlpatterns = [
	path('load_image/<int:pk>', load_image, name = 'load_image'),
	path('edit_image/<int:pk>', edit_image, name = 'edit_image'),
]

urlpatterns += [
	path('ajax/del-image/', ajax_del_image, name = 'ajax_del_image'),

]