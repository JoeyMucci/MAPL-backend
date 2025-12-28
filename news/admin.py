from django.contrib import admin
from .models import Reporter, Report, Referee

admin.site.register(Referee)
admin.site.register(Reporter)
admin.site.register(Report)
