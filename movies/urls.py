from django.urls import path
from django.conf.urls import url
from .views import view_movies, load_movie, edit_movie, ajax_del_movie

urlpatterns = [
	path('view_movies', view_movies, name = 'view_movies'),
	path('load_movie', load_movie, name = 'load_movie'),
	path('edit_movie/<int:pk>', edit_movie, name = 'edit_movie'),
]

urlpatterns += [
	path('ajax/del-movie/', ajax_del_movie, name = 'ajax_del_movie'),

]