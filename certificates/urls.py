from django.urls import path
from django.conf.urls import url
from .views import make_certificates


urlpatterns = [
	path('', make_certificates, name = 'make_certificates'),
]

