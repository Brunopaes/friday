import tensorflow as tf
import cv2

classes = [
    'wawaweewa',
    'non-wawaweewa'
]


def prepare(file):
    img_size = 50
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (img_size, img_size))
    return new_array.reshape(-1, img_size, img_size, 1)


model = tf.keras.models.load_model("CNN.model")

image = prepare(r"C:\Users\bruno\Desktop\a.jpg")

prediction = model.predict([image])
prediction = list(prediction[0])
print(classes[prediction.index(max(prediction))])
