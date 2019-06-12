from django.shortcuts import render
from .updateTables import updateTables
from .models import parkingLot, parkingSpot
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from datetime import datetime, timezone
from django.views.decorators.cache import never_cache


@never_cache # don't cache pictures - important for displaying updated pictures of lots
def parking(request):

	# get parkingLot and parkingSpot tables
	parking_lots = parkingLot.objects.all()
	parking_spots = parkingSpot.objects.all()

	# find elapsed time since images segmented
	now = datetime.now(timezone.utc)
	first_lot_time = parking_lots[0].lastUpdate
	elapsed_time = now - first_lot_time
	print(elapsed_time.seconds)
	# call updateTables() if it has been more than 600 seconds since the tables were last updated
	if(elapsed_time.seconds > 300):
		for p in parking_lots:
			parkingLot.objects.filter(lotName = p.lotName).update(lastUpdate=datetime.now(timezone.utc))
		updateTables()


	# get the parking lots longitude and latitude - needed since json encoding cannot encode Geoposition
	parking_lots_list = []
	for p in parking_lots:
		dictionary = {"lotName": p.lotName, "lat":p.lotPosition.latitude, "long":p.lotPosition.longitude}
		parking_lots_list.append(dictionary)
	parking_lots_json = json.dumps(parking_lots_list, cls=DjangoJSONEncoder)



	# static path for all of the images
	images = []
	for p in parking_lots:
		path = 'media/' + p.lotName + '_segmented.jpg'
		images.append(path)


	# get the parking spots longitude and latitude - needed since json encoding cannot encode Geoposition
	parking_spots_list = []
	for p in parking_spots:
		dictionary = {"lat":p.position.latitude, "long":p.position.longitude, "occupied":p.occupied}
		parking_spots_list.append(dictionary)
	parking_spots_json = json.dumps(parking_spots_list, cls=DjangoJSONEncoder) # turn paring_spots_list to json




	"""
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
	"""


	# return render of parking.html with context
	return render(request, 'parking/parking.html', context={"parking_lots":parkingLot.objects.all,
		"parking_spots":parkingSpot.objects.all,
		"images": images,
		"parking_spots_json":parking_spots_json,
		"parking_lots_json":parking_lots_json,
		})






