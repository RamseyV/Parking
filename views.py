from django.shortcuts import render
from .updateTables import updateTables
from .models import parkingLot, parkingSpot, occupiedHistory
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from datetime import date

from django.views.decorators.cache import never_cache


@never_cache # don't cache pictures - important for displaying updated pictures of lots
def parking(request):
	# updateTables()
	parking_lots = parkingLot.objects.all()
	parking_spots = parkingSpot.objects.all()
	occupied_history = occupiedHistory.objects.all()


	# static path for all of the images
	images = []
	for p in parking_lots:
		path = 'parking/images/' + p.lotName + '_segmented.jpg'
		images.append(path)


	# spot locations and occupied status for all spots 
	parking_spots_list = []

	for p in parking_spots:
		dictionary = {"lat":p.position.latitude, "long":p.position.longitude, "occupied":p.occupied}
		parking_spots_list.append(dictionary)
	parking_spots_json = json.dumps(parking_spots_list, cls=DjangoJSONEncoder) # turn paring_spots_list to json


	# get occupied history for today
	today = date.today()
	spots_for_today = occupiedHistory.objects.filter(time__year=today.year,time__month=today.month, time__day=today.day)

	print(spots_for_today)


	todays_spots = []
	for s in spots_for_today:
		s_time = s.time.time()
		s_time = "{:02d}".format(s_time.hour) + ":" + "{:02d}".format(s_time.minute) + ":" + "{:02d}".format(int(s_time.second))
		todays_spots.append({"date":s_time, "total": s.totalSpots})
		# todays_spots.append({"time":str(s.time.time()), "total": s.totalSpots})


	todays_spots = json.dumps(todays_spots) # turn todays spots to json file

	# return render of parking.html with context
	return render(request, 'parking/parking.html', context={"parking_lots":parkingLot.objects.all,
		"parking_spots":parkingSpot.objects.all,
		"occupied_history":occupied_history,
		"images": images,
		"parking_spots_json":parking_spots_json,
		"todays_spots":todays_spots})






