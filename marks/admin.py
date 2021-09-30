from django.contrib import admin
from .models import PictureMark, MovieMark


admin.site.register([PictureMark, MovieMark])
