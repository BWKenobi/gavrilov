from django.urls import path
from django.conf.urls import url
from .views import view_edit_profile, view_coprofiles, view_edit_coprofile, new_coprofile, ajax_del_coprofile

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
	path('view_coprofiles', view_coprofiles, name = 'view_coprofiles'),
	path('view_edit_coprofile/<int:pk>', view_edit_coprofile, name = 'view_edit_coprofile'),
	path('new_coprofile', new_coprofile, name = 'new_coprofile'),
]

urlpatterns += [
	path('ajax/del-coprofile/', ajax_del_coprofile, name = 'ajax_del_coprofile'),

]