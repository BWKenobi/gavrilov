from django.urls import path
from django.conf.urls import url
from .views import view_edit_profile, view_new_admin_profile
from .views import view_coprofiles, view_edit_profile_admin, view_edit_coprofile, view_edit_coprofile_admin, new_coprofile, new_coprofile_admin
from .views import view_team_coprofiles, view_edit_team_coprofile, view_edit_team_coprofile_admin, new_team_coprofile, new_team_coprofile_admin

from .views import view_comings
from .views import ajax_del_coprofile, change_come_flag

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
	path('new_admin_profile', view_new_admin_profile, name = 'view_new_admin_profile'),
	path('view_admin_edit_profile/<int:pk>', view_edit_profile_admin, name = 'view_edit_profile_admin'),

	path('view_coprofiles', view_coprofiles, name = 'view_coprofiles'),
	path('view_edit_coprofile/<int:pk>', view_edit_coprofile, name = 'view_edit_coprofile'),
	path('view_edit_coprofile_admin/<int:pk>', view_edit_coprofile_admin, name = 'view_edit_coprofile_admin'),

	path('new_coprofile', new_coprofile, name = 'new_coprofile'),
	path('new_coprofile_admin', new_coprofile_admin, name = 'new_coprofile_admin'),
	path('new_coprofile_admin/<int:pk>', new_coprofile_admin, name = 'new_coprofile_admin'),

	path('view_team_coprofiles', view_team_coprofiles, name = 'view_team_coprofiles'),
	path('view_edit_team_coprofile/<int:pk>', view_edit_team_coprofile, name = 'view_edit_team_coprofile'),
	path('view_edit_team_coprofile_admin/<int:pk>', view_edit_team_coprofile_admin, name = 'view_edit_team_coprofile_admin'),

	path('new_team_coprofile', new_team_coprofile, name = 'new_team_coprofile'),
	path('new_team_coprofile_admin', new_team_coprofile_admin, name = 'new_team_coprofile_admin'),
	path('new_team_coprofile_admin/<int:pk>', new_team_coprofile_admin, name = 'new_team_coprofile_admin'),

	path('view_comings', view_comings, name = 'view_comings'),
]

urlpatterns += [
	path('ajax/del-coprofile/', ajax_del_coprofile, name = 'ajax_del_coprofile'),
	path('ajax/change-come-flag/', change_come_flag, name = 'ajax_change_come_flag'),
]
