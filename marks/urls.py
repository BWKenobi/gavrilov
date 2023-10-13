from django.urls import path
from django.conf.urls import url
from .views import mark_card
from .views import ajax_set_marks, ajax_set_pict_marks, ajax_set_pict_far_marks, ajax_set_movie_far_marks

urlpatterns = [
	path('mark_card', mark_card, name = 'mark_card'),
]

urlpatterns += [
	path('ajax/set-marks/', ajax_set_marks, name = 'ajax_set_marks'),
	path('ajax/set-pict-marks/', ajax_set_pict_marks, name = 'ajax_set_pict_marks'),
	path('ajax/set-pict-far-marks/', ajax_set_pict_far_marks, name = 'ajax_set_pict_far_marks'),
	path('ajax/set-movie-far-marks/', ajax_set_movie_far_marks, name = 'ajax_set_movie_far_marks'),
]
