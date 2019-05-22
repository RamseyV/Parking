from django.contrib import admin
from .models import parkingLot, parkingSpot, occupiedHistory

# class WCUClassesAdmin(admin.ModelAdmin):
# 	 fieldsets = [
#         ("Class Name", {'fields': ["name"]}),
#         ("Description", {'fields': ["description"]}),
#         ("Subject", {'fields': ["subject"]}),
#         ("Languages", {"fields": ["languages"]})
#     ]


# admin.site.register(Subjects)


admin.site.register(parkingLot)
admin.site.register(parkingSpot)
admin.site.register(occupiedHistory)