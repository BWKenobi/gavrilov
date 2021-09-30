from django.urls import path
from django.conf.urls import url
from .views import view_art_nomination, view_mov_nomination

urlpatterns = [
	path('view-art-nomination/<int:pk>', view_art_nomination, name = 'view_art_nomination'),
	path('view-mov-nomination/<int:pk>', view_mov_nomination, name = 'view_mov_nomination'),
]
