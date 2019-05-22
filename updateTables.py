from .models import parkingLot, parkingSpot
import requests
from PIL import Image
from .Mask_RCNN.segmentImages import segmentImages
from io import BytesIO
import cv2
import numpy as np


class updateTables():


	def __init__(self):
		self.parking_lots = parkingLot.objects.all()
		urls = self.getURLs()
		images = self.scrapeImages(urls)

		############## Uncomment this for testing puposes #################
		# images = self.test_M1_lot()

		results, segmented_images = self.getSegmentation(images)
		rois = []

		for r in results:
			rois.append(r['rois'])

		print("Rois:", rois)
		self.findOccupiedSpots(rois)
		self.updateImages(images, segmented_images)
		# self.updateOccupiedHistory(results)



	# Strictly for testing purposes - only to be used when only M1 lot is in database
	def test_M1_lot(self):
		images = []
		img = Image.open('/Users/ramseyvillarreal/Dropbox/WCUPA/M-1Lot.jpg')
		images.append(np.array(img))
		return images

	# Get the urls where the images are in the parkingLot table - 'imageURL' field
	def getURLs(self):
		urls = [p.imageURL for p in self.parking_lots]
		return urls

	# Download the images from the urls 
	def scrapeImages(self, urls):
		images = []
		for u in urls:
			response = requests.get(u)
			img = Image.open(BytesIO(response.content))
			images.append(np.array(img))
		return images


	# Call script to segment image 
	def getSegmentation(self, imgs):
		# cv2.imshow(imgs[0])
		print(type(imgs[0]))
		sI = segmentImages()
		results, segmented_images = sI.segment(imgs)
		return results, segmented_images
		


	"""
	# updates 'image' and 'segmentedImage' in parkingLot
	def updateImages(self, image, segmentedImage):
		i=0
		for p in self.parking_lots:
			# p.image = image[i]
			# p.segmentedImage = segmentedImage[i]
			img = Image.fromarray(image[i])
			img_dir = '/Users/ramseyvillarreal/Dropbox/mysite/parking/static/parking/images/'
			img.save(img_dir + p.lotName+'.jpg')
			# simg = Image.open(segmentedImage[i])
			segmentedImage[i].save(img_dir+ p.lotName+'_segmented.jpg')
			parkingLot.objects.filter(lotName=p.lotName).update(image=img_dir + p.lotName+'.jpg',
			segmentedImage=img_dir+ p.lotName+'_segmented.jpg')			
			i+=1
		
	"""

	"""
	# Updates any occupied spots in the occupiedHistory table
	def updateOccupiedHistory(self,results):
		# spots = parkingSpot.objects.all()
		total = 0
		# for spot in spots:
		# 	if(spot.occupied == 1):
		# 		total+=1


		for r in results:
			for i, ids in enumerate(r['class_ids']):
				print(ids)
				if (ids==3 or ids==4 or ids==8):
					total+=1

		print(total)
		entry = occupiedHistory.create(totalSpots=total)
		entry.save()
		
	"""

	# get the x and y coordinates of the spots from parkingLot table - returns list of tuples in form of [(x1,y1), (x2,y2) ... ]
	def getPixelLocations(self, pkLot):
		spot_locations = [(p.x,p.y) for p in self.parkingLot if p.lot == pkLot]
		return spot_locations


	# Determine if a spot location is being covered by a car
	def findOccupiedSpots(self, rois):
		i=0
		for p in self.parking_lots:	
			spots = parkingSpot.objects.filter(lot=p)
			spot_locations = [(p.x,p.y) for p in spots]
			current_rois = rois[i]

			# Set all of the spots to not occupied
			for spot in spots:
				parkingSpot.objects.filter(x=spot.x, y=spot.y).update(occupied=False)


			for roi in current_rois:
				canidates = []
				for spot in spots:
					# roi[1] = smallest x value (leftmost on image)
					# roi[3] = greatest x value (rightmost on image)
					# roi[0] = smallest y value (highest on image)
					# roi[2] = greatest y value (lowest on image)
					if(spot.x > roi[1] and spot.x < roi[3] and spot.y >roi[0] and spot.y<roi[2]):
						canidates.append({'x':spot.x,'y':spot.y})
						# parkingSpot.objects.filter(x=spot.x, y=spot.y).update(occupied=True)
				
				if(len(canidates) == 0 ):
					for spot in spots:	
						if(spot.x > roi[1] and spot.x < roi[3]):
							car_height = roi[2] - roi[0]
							if(spot.y > roi[0] and spot.y < (roi[2]+car_height)):
								canidates.append({'x':spot.x,'y':spot.y})


				if(len(canidates) > 0):

					for i, can in enumerate(canidates):
						if(i==0):
							lowest_canidate = can
						else:
							if(can.get('y') > lowest_canidate.get('y')):
								lowest_canidate = can

					parkingSpot.objects.filter(x=lowest_canidate.get('x'), y=lowest_canidate.get('y')).update(occupied=True)
					# else:
					# 	parkingSpot.objects.filter(x=spot.x, y=spot.y).update(occupied=False)


			i+=1
					

		





if __name__ == '__main__':
	updateTables()
