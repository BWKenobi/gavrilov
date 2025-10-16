from django.urls import path
from django.conf.urls import url
from .views import view_serificates, view_my_serificates, generate_sertificates, del_serificates, send_serificates

urlpatterns = [
	path('', view_serificates, name = 'view_serificates'),
	path('my_serificates', view_my_serificates, name = 'view_my_serificates'),
	path('del_serificates', del_serificates, name = 'del_serificates'),
	path('send_serificates', send_serificates, name = 'send_serificates'),
]

urlpatterns += [
	path('ajax/generate-sertificates/', generate_sertificates, name = 'generate_sertificates'),
]
