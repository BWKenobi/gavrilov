from django.urls import path
from django.conf.urls import url
from .views import mark_card
from .views import ajax_set_marks

urlpatterns = [
	path('mark_card', mark_card, name = 'mark_card'),
]

urlpatterns += [
	path('ajax/set-marks/', ajax_set_marks, name = 'ajax_set_marks'),

]