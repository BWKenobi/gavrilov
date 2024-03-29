from django.urls import path
from django.conf.urls import url
from .views import view_art_nomination, view_movie_nomination, view_art_far_nomination, view_movie_far_nomination

urlpatterns = [
	path('view-art-nomination/<int:pk>', view_art_nomination, name = 'view_art_nomination'),
	path('view-movie-nomination/<int:pk>', view_movie_nomination, name = 'view_movie_nomination'),
	path('view-art-far-nomination/', view_art_far_nomination, name = 'view_art_far_nomination'),
	path('view-art-far-nomination/<int:pk>', view_art_far_nomination, name = 'view_art_far_nomination'),
	path('view-movie-far-nomination/', view_movie_far_nomination, name = 'view_movie_far_nomination'),
	path('view-movie-far-nomination/<int:pk>', view_movie_far_nomination, name = 'view_movie_far_nomination'),

]

