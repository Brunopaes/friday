from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

import matplotlib.pyplot as plt
import pickle
import numpy

# Opening the files about data
X = numpy.array(pickle.load(open("X.pickle", "rb")))
y = numpy.array(pickle.load(open("y.pickle", "rb")))

# normalizing data (a pixel goes from 0 to 255)
X = X/255.0

# Building the model
model = Sequential()
# 3 convolutional layers
model.add(layers.Conv2D(32, (3, 3), input_shape=X.shape[1:]))
model.add(layers.Activation("relu"))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3)))
model.add(layers.Activation("relu"))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3)))
model.add(layers.Activation("relu"))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.25))

# 2 hidden layers
model.add(layers.Flatten())
model.add(layers.Dense(128))
model.add(layers.Activation("relu"))

model.add(layers.Dense(128))
model.add(layers.Activation("relu"))


# The output layer with 2 neurons, for 2 classes
model.add(layers.Dense(2))
model.add(layers.Activation("sigmoid"))

# Compiling the model using some basic parameters
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

# Training the model, with 40 iterations
# validation_split corresponds to the percentage of images
# used for the validation phase compared to all the images
history = model.fit(X, y, batch_size=32, epochs=40, validation_split=0.1,
                    use_multiprocessing=True)

# Saving the model
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

model.save_weights("model.h5")
print("Saved model to disk")

model.save('CNN.model')

# Printing a graph showing the accuracy changes during the training phase
print(history.history.keys())
plt.figure(1)
plt.plot(history.history['val_accuracy'])
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
