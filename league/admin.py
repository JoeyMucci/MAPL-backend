from django.contrib import admin
from .models import Pebbler, Bout, Performance

admin.site.register(Pebbler)

admin.site.register(Performance)


class BoutAdmin(admin.ModelAdmin):
    list_display = ['ability_activated']

    def ability_activated(self, obj):
        return obj.away_roll != obj.away_roll_half or obj.home_roll != obj.home_roll_final
    ability_activated.boolean = True
    ability_activated.short_description = 'Ability Activated'

admin.site.register(Bout, BoutAdmin)