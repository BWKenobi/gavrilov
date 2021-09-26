from django.contrib import admin
from .models import ArtNomination, VocalNomination


admin.site.register({ArtNomination, VocalNomination})
