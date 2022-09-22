from django.contrib import admin
from .models import Movie, CoMovie


admin.site.register({Movie, CoMovie})
