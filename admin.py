from django.contrib import admin
from .models import parkingLot, parkingSpot

# class WCUClassesAdmin(admin.ModelAdmin):
# 	 fieldsets = [
#         ("Class Name", {'fields': ["name"]}),
#         ("Description", {'fields': ["description"]}),
#         ("Subject", {'fields': ["subject"]}),
#         ("Languages", {"fields": ["languages"]})
#     ]


# admin.site.register(Subjects)
'''
class ParkingAdmin(admin.ModelAdmin):
    class Media:
        js = (settings.STATIC_URL + "geoposition/geoposition.js",)
'''

admin.site.register(parkingLot)
admin.site.register(parkingSpot)
# admin.site.register(occupiedHistory)
