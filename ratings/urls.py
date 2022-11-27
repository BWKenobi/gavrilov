from django.urls import path
from django.conf.urls import url
from .views import view_art_nomination, view_mov_nomination, view_protocols, get_check_list

urlpatterns = [
	path('view-art-nomination/<int:pk>', view_art_nomination, name = 'view_art_nomination'),
	path('view-mov-nomination/<int:pk>', view_mov_nomination, name = 'view_mov_nomination'),
	path('view-protocols', view_protocols, name = 'view_protocols'),
	path('get-check-list/<int:pk>', get_check_list, name = 'get_check_list'),
]
