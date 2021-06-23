import cv2
import tensorflow as tf

CAT = ['Grenades', 'Knives', 'Machine Guns', 'Pistol Hand Guns', 'RPGs']
model = tf.keras.models.load_model('model.h5')

def prepare(image):
    size = 32;
    img = image;
    new_img = cv2.resize(img, (size,size))
    return new_img.reshape(-1,size,size,1)


def predict(image):
    prediction = model.predict(prepare(image))
    print(prediction)
    for i in range(0,5):
        if(int(prediction[0][i]) == 1):
            return CAT[i]