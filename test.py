from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow import keras
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os


args = {'dataset': 'data\\train', 'model': 'model.h5', 'label_bin': 'bin', 'plot': 'plot'}

# initialize the data and labels
print("[INFO] loading images...")
data = []
labels = []
num_classes = 6

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
    print(imagePath)
    # load the image, resize the image to be 32x32 pixels (ignoring
    # aspect ratio), flatten the image into 32x32x1=1024 pixel image
    # into a list, and store the image in the data list
    try:
        image = cv2.imread(imagePath, 0)
        image = cv2.resize(image, (64, 64))
        image = np.reshape(image, (64, 64, 1))
        data.append(image)
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)
    except Exception as e:
        print(str(e))

    # extract the class label from the image path and update the
    # labels list

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data,
    labels, test_size=0.2, random_state=42)

print(trainX.max())
trainX = trainX / 255
testX = testX / 255
print(trainX.shape)
print(testX.shape)
plt.imshow(testX[0])
plt.show()
print(testY)