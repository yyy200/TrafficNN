import cv2

import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from sklearn.model_selection import train_test_split

MAX_EPOCHS = 51
MAX_NODES = 3
MAX_LAYERS = 2
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python traffic.py data_directory")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    for epochs in range(50, MAX_EPOCHS):
        for layer in range(1, MAX_LAYERS):
            for nodes in range(1, MAX_NODES):
                # Split data into training and testing sets
                labels = tf.keras.utils.to_categorical(labels)
                x_train, x_test, y_train, y_test = train_test_split(
                    np.array(images), np.array(labels), test_size=TEST_SIZE
                )

                # Get a compiled neural network
                model = get_model(layer, nodes)

                # Fit model on training data
                model.fit(x_train, y_train, epochs=epochs)

                # Evaluate neural network performance
                model.evaluate(x_test,  y_test, verbose=2)

                model.save(f"e{epochs}-l{layer}-n{nodes}.h5")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()

    for i in range(NUM_CATEGORIES):
        j = 0
        while True:
            for k in range(30):
                img = cv2.imread(os.path.join(data_dir,str(i),f"{str(j).zfill(5)}_{str(k).zfill(5)}.ppm"))

                if type(img) != np.ndarray:
                    break

                images.append(cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT)))
                labels.append(i)

            if type(img) != np.ndarray:
                    break
            j += 1
    print(len(images), ":", len(labels))
    return images, labels

def get_model(layer_number, nodes):
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = keras.Sequential([
        layers.Conv2D(5356, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.MaxPooling2D(pool_size=(3, 3)),
        layers.Flatten()  
    ])
    for i in range(layer_number):
        model.add(layers.Dense(nodes, activation="relu"))
    
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.build(input_shape=(layer_number, nodes))

    model.summary()
    
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model
if __name__ == "__main__":
    main()