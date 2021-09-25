from django.urls import path
from django.conf.urls import url
from .views import new_teacher, view_teacher, edit_teacher

urlpatterns = [
	path('new_teacher', new_teacher, name = 'new_teacher'),
	path('view_teacher/<int:pk>', view_teacher, name = 'view_teacher'),
	path('edit_teacher/<int:pk>', edit_teacher, name = 'edit_teacher'),
]
