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
import random
import pickle
import cv2
import os




args = {'dataset':'static/data/train','model':'normal.h5', 'label_bin':'bin', 'plot':'plot'}


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
        image = cv2.resize(image, (32, 32))
        image = np.reshape(image, (32, 32, 1))
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

# convert the labels from integers to vectors (for 2-class, binary
# classification you should use Keras' to_categorical function
# instead as the scikit-learn's LabelBinarizer will not return a
# vector)
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Initialising the CNN
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape = (32,32,1), activation = 'relu'))

model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(units = 128, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(units=num_classes, activation = 'softmax'))

model.summary()

# initialize our initial learning rate and # of epochs to train for
INIT_LR = 0.0001
EPOCHS = 50

# Compiling the CNN
opt = keras.optimizers.RMSprop(lr=INIT_LR, decay=1e-6)
model.compile(optimizer = opt, loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the CNN to the images
H = model.fit(trainX, trainY, validation_data=(testX, testY), epochs=EPOCHS, batch_size=32)

# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1),
    predictions.argmax(axis=1), target_names=lb.classes_))

# plot the training loss and accuracy
N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.plot(N, H.history["accuracy"], label="train_acc")
plt.plot(N, H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy (Simple NN)")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig(args["plot"])

# save the model and label binarizer to disk
print("[INFO] serializing network and label binarizer...")
model.save(args["model"])
f = open(args["label_bin"], "wb")
f.write(pickle.dumps(lb))
f.close()