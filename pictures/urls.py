from django.urls import path
from django.conf.urls import url
from .views import view_arts, load_image, edit_image, ajax_del_image

urlpatterns = [
	path('view_arts', view_arts, name = 'view_arts'),
	path('load_image', load_image, name = 'load_image'),
	path('edit_image/<int:pk>', edit_image, name = 'edit_image'),
]

urlpatterns += [
	path('ajax/del-image/', ajax_del_image, name = 'ajax_del_image'),

]