from django.contrib import admin
from .models import Pebbler, Bout, Performance

admin.site.register(Pebbler)

admin.site.register(Performance)


class BoutAdmin(admin.ModelAdmin):
    list_display = ['division', 'quirk_activated', 'ability_activated']

    def quirk_activated(self, obj):
        return obj.away_quirk or obj.home_quirk
    quirk_activated.boolean = True
    quirk_activated.short_description = 'Quirk Activated'

    def ability_activated(self, obj):
        return obj.away_roll != obj.away_roll_half or obj.home_roll != obj.home_roll_final
    ability_activated.boolean = True
    ability_activated.short_description = 'Ability Activated'

admin.site.register(Bout, BoutAdmin)