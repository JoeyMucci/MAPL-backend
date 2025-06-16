from django.contrib import admin
from .models import Pebbler, Bout, Performance

admin.site.register(Pebbler)

admin.site.register(Performance)


class BoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'division', 'quirk_activated_h', 'ability_activated_h', 'quirk_activated_a', 'ability_activated_a']
    list_filter = ['division', 'home_quirk', 'home_ability', 'away_quirk', 'away_ability']

    def quirk_activated_a(self, obj):
        return obj.away_quirk
    quirk_activated_a.boolean = True
    quirk_activated_a.short_description = 'Away quirk'

    def ability_activated_a(self, obj):
        return obj.away_ability
    ability_activated_a.boolean = True
    ability_activated_a.short_description = 'Away ability'

    def quirk_activated_h(self, obj):
        return obj.home_quirk
    quirk_activated_h.boolean = True
    quirk_activated_h.short_description = 'Home quirk'

    def ability_activated_h(self, obj):
        return obj.home_ability
    ability_activated_h.boolean = True
    ability_activated_h.short_description = 'Home ability'

admin.site.register(Bout, BoutAdmin)