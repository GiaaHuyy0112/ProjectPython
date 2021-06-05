import cv2
import tensorflow as tf

CATEGORIES = ["Grenades", "Knives", "Machine Guns", "Masked Face", "Pistol Hand Guns", "RPG"]


def prepare(filepath):
    IMG_SIZE = 32  # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


model = tf.keras.models.load_model("model.h5")
# model.summary()

prediction = model.predict(prepare('data/test/Machine Guns/122.jpg'))
print(prediction)  # will be a list in a list.
for i in range(0,6):
    if(int(prediction[0][i]) == 1):
        # print(CATEGORIES[int(prediction[0][i])])
        print(CATEGORIES[i])