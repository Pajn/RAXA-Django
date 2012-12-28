from django.contrib import admin
from models import Floor, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 10

class FloorAdmin(admin.ModelAdmin):
    inlines = [RoomInline]
    list_display = ('name', 'num_rooms')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor')
    list_filter = ['floor']

admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)