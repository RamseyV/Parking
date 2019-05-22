from django.shortcuts import render
from .updateTables import updateTables
from .models import parkingLot, parkingSpot, occupiedHistory
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from datetime import date

from django.views.decorators.cache import never_cache


def occupied_history_json(request):

	occupied_history = occupiedHistory.objects.all()

	occupied = {}
	for o in occupied_history:
	
		try:
			if(str(o.time.date()) in occupied):
				occupied[str(o.time.date())] += o.totalSpots
			else:
				occupied[str(o.time.date())] =  o.totalSpots

		except AttributeError:
			print("Didn't work for ", o)
		

	return JsonResponse(occupied, safe=False)

@never_cache
def parking(request):
	# updateTables()
	parking_lots = parkingLot.objects.all()
	parking_spots = parkingSpot.objects.all()
	occupied_history = occupiedHistory.objects.all()


	images = []
	for p in parking_lots:
		path = 'parking/images/' + p.lotName + '_segmented.jpg'
		images.append(path)


	
	parking_spots_list = []

	for p in parking_spots:
		dictionary = {"lat":p.position.latitude, "long":p.position.longitude, "occupied":p.occupied}
		parking_spots_list.append(dictionary)
	parking_spots = json.dumps(parking_spots_list, cls=DjangoJSONEncoder)

	


	# get all of occupied history for today
	occupied = {}
	for o in occupied_history:
	
		try:
			if(str(o.time.date()) in occupied):
				occupied[str(o.time.date())] += o.totalSpots
			else:
				occupied[str(o.time.date())] =  o.totalSpots

		except AttributeError:
			print("Didn't work for ", o)
	
	occupied_list = []
	for k,v in occupied.items():
		occupied_list.append({"date": k, "total": v})

	occupied_json = json.dumps(occupied_list) # turn occupied list into json




	today = date.today()
	spots_for_today = occupiedHistory.objects.filter(time__year=today.year,time__month=today.month, time__day=today.day)

	print(spots_for_today)


	todays_spots = []
	for s in spots_for_today:
		s_time = s.time.time()
		s_time = "{:02d}".format(s_time.hour) + ":" + "{:02d}".format(s_time.minute) + ":" + "{:02d}".format(int(s_time.second))
		todays_spots.append({"date":s_time, "total": s.totalSpots})
		# todays_spots.append({"time":str(s.time.time()), "total": s.totalSpots})


	todays_spots = json.dumps(todays_spots)


	return render(request, 'parking/parking.html', context={"parking_lots":parkingLot.objects.all,
		"parking_spots":parkingSpot.objects.all,
		"occupied_history":occupiedHistory.objects.all,
		"images": images,
		"parking_spots_json":parking_spots,
		"occupied_json":occupied_json,
		"todays_spots":todays_spots})






