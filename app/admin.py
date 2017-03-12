from django.contrib import admin
from app import models

admin.site.register(models.User)
admin.site.register(models.Event)
admin.site.register(models.Bet)
admin.site.register(models.Team)
