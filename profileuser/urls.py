from django.urls import path
from django.conf.urls import url
from .views import view_edit_profile, view_coprofiles, view_edit_coprofile, view_edit_coprofile_admin, new_coprofile, new_coprofile_admin, ajax_del_coprofile, view_comings, change_come_flag

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
	path('view_coprofiles', view_coprofiles, name = 'view_coprofiles'),
	path('view_edit_coprofile/<int:pk>', view_edit_coprofile, name = 'view_edit_coprofile'),
	path('view_edit_coprofile_admin/<int:pk>', view_edit_coprofile_admin, name = 'view_edit_coprofile_admin'),
	path('new_coprofile', new_coprofile, name = 'new_coprofile'),
	path('new_coprofile_admin', new_coprofile_admin, name = 'new_coprofile_admin'),
	path('new_coprofile_admin/<int:pk>', new_coprofile_admin, name = 'new_coprofile_admin'),
	path('view_comings', view_comings, name = 'view_comings'),
]

urlpatterns += [
	path('ajax/del-coprofile/', ajax_del_coprofile, name = 'ajax_del_coprofile'),
	path('ajax/change-come-flag/', change_come_flag, name = 'ajax_change_come_flag'),
]