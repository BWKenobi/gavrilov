from django.urls import path
from django.conf.urls import url
from .views import view_arts, view_arts_admin, load_image, load_image_admin, edit_image, edit_image_admin, ajax_del_image

urlpatterns = [
	path('view_arts', view_arts, name = 'view_arts'),
	path('view_arts_admin/<int:pk>', view_arts_admin, name = 'view_arts_admin'),

	path('load_image', load_image, name = 'load_image'),
	path('load_image_admin', load_image_admin, name = 'load_image_admin'),
	path('load_image_admin/<int:pk>', load_image_admin, name = 'load_image_admin'),

	path('edit_image/<int:pk>', edit_image, name = 'edit_image'),
	path('edit_image_admin', edit_image_admin, name = 'edit_image_admin'),
	path('edit_image_admin/<int:pk>', edit_image_admin, name = 'edit_image_admin'),
]

urlpatterns += [
	path('ajax/del-image/', ajax_del_image, name = 'ajax_del_image'),

]
