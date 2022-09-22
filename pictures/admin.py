from django.contrib import admin
from .models import Picture, CoPicturee


admin.site.register({Picture, CoPicturee})
