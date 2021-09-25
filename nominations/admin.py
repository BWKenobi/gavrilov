from django.contrib import admin
from .models import Nomination, SubNomination


admin.site.register({Nomination, SubNomination})
