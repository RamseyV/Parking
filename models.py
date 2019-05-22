from django.db import models
from geoposition.fields import GeopositionField
from geoposition import Geoposition
from datetime import datetime
# Create your models here.

class parkingLot(models.Model):
	lotName = models.CharField(max_length=200)
	numSpots = models.IntegerField()
	occupiedSpots = models.IntegerField()
	imageURL = models.URLField(max_length=200)
	image = models.ImageField(blank=True, null=True)
	segmentedImage = models.ImageField(blank=True,null=True)
	def __str__(self):
		return self.lotName


class parkingSpot(models.Model):
	"""docstring for parkingSpot"""
	x = models.IntegerField()
	y = models.IntegerField()
	# longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
	# latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
	position = GeopositionField(default='39.958, -75.601',null=True, blank=True)
	occupied = models.BooleanField(default=False)
	lot = models.ForeignKey(parkingLot, blank=True, null=True, on_delete=models.SET_NULL)
	
	
class occupiedHistory(models.Model):
	time = models.DateTimeField(default=datetime.now(), blank=True)
	totalSpots = models.IntegerField(null=True)

	@classmethod
	def create(cls, totalSpots):
		occupiedHistory = cls(totalSpots=totalSpots)
		return occupiedHistory

