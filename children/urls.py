from django.urls import path
from django.conf.urls import url
from .views import new_child, view_child, edit_child

urlpatterns = [
	path('new_child', new_child, name = 'new_child'),
	path('view_child/<int:pk>', view_child, name = 'view_child'),
	path('edit_child/<int:pk>', edit_child, name = 'edit_child'),
]
