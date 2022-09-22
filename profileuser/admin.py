from django.contrib import admin
from .models import Profile, CoProfile


admin.site.register({Profile, CoProfile})
