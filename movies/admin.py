from django.contrib import admin

from . import models


admin.site.register(models.Movie)
admin.site.register(models.Person)
admin.site.register(models.TVShow)
admin.site.register(models.TVShowSeason)
