from tqdm import tqdm

import numpy as np
import pickle
import random
import cv2
import os


file_list = []
class_list = []

data_dir = "data"

# All the categories you want your neural network to detect
classes = [
	'wawaweewa',
	'non-wawaweewa'
]

# The size of the images that your neural network will use
img_size = 50

# Checking or all images in the data folder
for class_ in classes:
	path = os.path.join(data_dir, class_)
	for img in tqdm(os.listdir(path), desc='Data Read'):
		img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)

training_data = []


def create_training_data():
	for category_ in classes:
		path_ = os.path.join(data_dir, class_)
		class_num = classes.index(category_)
		for img_ in tqdm(os.listdir(path_), desc='Train Data Creation'):
			try:
				img_array_ = \
					cv2.imread(os.path.join(path_, img_), cv2.IMREAD_GRAYSCALE)
				new_array = cv2.resize(img_array_, (img_size, img_size))
				training_data.append([new_array, class_num])
			except Exception as e:
				pass


create_training_data()


random.shuffle(training_data)

X = []  # features
y = []  # labels

for features, label in training_data:
	X.append(features)
	y.append(label)

X = np.array(X).reshape(-1, img_size, img_size, 1)

# Creating the files containing all the information about your model
pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)
