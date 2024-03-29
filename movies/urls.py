from django.urls import path
from django.conf.urls import url
from .views import view_movies, view_movies_admin, load_movie, load_movie_admin, edit_movie, edit_movie_admin, ajax_del_movie, ajax_change_scene_movie

urlpatterns = [
	path('view_movies', view_movies, name = 'view_movies'),
	path('view_movies_admin/<int:pk>', view_movies_admin, name = 'view_movies_admin'),

	path('load_movie', load_movie, name = 'load_movie'),
	path('load_movie_admin', load_movie_admin, name = 'load_movie_admin'),
	path('load_movie_admin/<int:pk>', load_movie_admin, name = 'load_movie_admin'),

	path('edit_movie/<int:pk>', edit_movie, name = 'edit_movie'),
	path('edit_movie_admin', edit_movie_admin, name = 'edit_movie_admin'),
	path('edit_movie_admin/<int:pk>', edit_movie_admin, name = 'edit_movie_admin'),
]

urlpatterns += [
	path('ajax/del-movie/', ajax_del_movie, name = 'ajax_del_movie'),
	path('ajax/change-scene-movie/', ajax_change_scene_movie, name = 'ajax_change_scene_movie'),

]
