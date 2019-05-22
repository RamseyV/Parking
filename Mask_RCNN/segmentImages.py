import os

# ROOT_DIR = os.getcwd()
# os.chdir(ROOT_DIR + '/parking/Mask_RCNN-master')


import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from . import coco
from . import utils
from . import model as modellib
from . import visualize

import tensorflow as tf
from keras.backend import clear_session

# clear_session()

# Root directory of the project

# ROOT_DIR =  'C:/Users/ramse/Dropbox/mysite/parking/'
# Directory to save logs and trained model
MODEL_DIR = '/Users/ramseyvillarreal/Dropbox/mysite/parking/Mask_RCNN/logs'
# print(MODEL_DIR)
# Local path to trained weights file
COCO_MODEL_PATH = '/Users/ramseyvillarreal/Dropbox/mysite/parking/Mask_RCNN/mask_rcnn_coco.h5'
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
		utils.download_trained_weights(COCO_MODEL_PATH)


class InferenceConfig(coco.CocoConfig):
		# Set batch size to 1 since we'll be running inference on
		# one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
		GPU_COUNT = 1
		IMAGES_PER_GPU = 1


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
							 'bus', 'train', 'truck', 'boat', 'traffic light',
							 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
							 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
							 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
							 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
							 'kite', 'baseball bat', 'baseball glove', 'skateboard',
							 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
							 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
							 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
							 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
							 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
							 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
							 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
							 'teddy bear', 'hair drier', 'toothbrush']


class segmentImages():
	"""docstring for segmentImages"""
	def segment(self, images):

		clear_session()
		config = InferenceConfig()
		config.display()

		# Create model object in inference mode.
		model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

		# Load weights trained on MS-COCO
		model.load_weights(COCO_MODEL_PATH, by_name=True)
		# graph = tf.get_default_graph()

		segmented = []
		results = []
		for i in images:
			# global graph
			# with graph.as_default():
			r = model.detect([i],verbose=1)
			print("R: ", r[0])
			r = r[0]
			segment = visualize.display_instances(i, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
			segmented.append(segment)
			results.append(r)



		return results, segmented


		



