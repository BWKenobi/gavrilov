from django.urls import path
from django.conf.urls import url
from .views import view_art_nomination, view_mov_nomination, view_protocols, get_check_list, get_protocol_pic#, get_protocol_mov
from .views import ajax_change_pic_place, ajax_change_mov_place

urlpatterns = [
	path('view-art-nomination/<int:pk>', view_art_nomination, name = 'view_art_nomination'),
	path('view-mov-nomination/<int:pk>', view_mov_nomination, name = 'view_mov_nomination'),
	path('view-protocols', view_protocols, name = 'view_protocols'),
	path('get-check-list/<int:pk>/<str:param>', get_check_list, name = 'get_check_list'),
	path('get_protocol_pic', get_protocol_pic, name = 'get_protocol_pic'),
	#path('get_protocol_mov', get_protocol_mov, name = 'get_protocol_mov'),
]

urlpatterns += [
	path('ajax/change-pic-place/', ajax_change_pic_place, name = 'ajax_change_pic_place'),
	path('ajax/change-mov-place/', ajax_change_mov_place, name = 'ajax_change_mov_place'),
]
