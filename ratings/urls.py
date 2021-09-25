from django.urls import path
from django.conf.urls import url
from .views import view_nomination, view_subnomination, view_master

urlpatterns = [
	path('view-nomination/<int:pk>', view_nomination, name = 'view_nomination'),
	path('view-subnomination/<int:pk>', view_subnomination, name = 'view_subnomination'),
	path('view-master', view_master, name = 'view_master'),
]
