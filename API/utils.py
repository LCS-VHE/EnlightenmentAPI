"""
A list of useful functions that the api would use
"""
import os
from PIL import Image
import numpy as np
from joblib import load
from tensorflow import keras
from constants import PLACEHOLDING_DATA_DIR
import time

"""
A list of global variables
"""
autoencoder = keras.models.load_model(os.path.join(os.curdir, "Models", "Best Model.h5"),custom_objects={"rounded_accuracy": lambda x: x})
decoder = autoencoder.layers[1]
pca = load(os.path.join(os.curdir, "Models", 'Trained .joblib'))

mins = []
maxs = []

def init():
    """
    initialized data
    :return:
    """
    global mins, maxs
    config_dir = os.path.join(os.curdir, "Models")
    with open(os.path.join(config_dir, "Max.txt"), "r") as max:
        with open(os.path.join(config_dir, "Min.txt"), "r") as min:

            for lin in max.readlines():
                maxs.append(float(lin))

            for lin in min.readlines():
                mins.append(float(lin))

def save_anime_face(sliders, loc=False):
    """
    Saving the anime face from the data
    :param sliders:
    :return:
    """
    if not loc: # With no defined path
        img = []
        filename = f"Anime Face{time.time()}.png" # The format of the anime face
        for index in range(len(sliders)):
            img.append(sliders[index] / 10 * (maxs[index] - mins[index]))

        img = pca.inverse_transform([img])
        img = decoder.predict(img).reshape((64, 64, 3))

        img = np.clip(img, 0, 1)
        img = Image.fromarray((img*255).astype(np.uint8))
        img.save(os.path.join(PLACEHOLDING_DATA_DIR, filename))
        return filename
    else:
        img = []
        for index in range(33):
            img.append(sliders[index] / 10 * (maxs[index] - mins[index]))

        img = pca.inverse_transform([img])
        img = decoder.predict(img).reshape((64, 64, 3))

        img = np.clip(img, 0, 1)
        img = Image.fromarray((img * 255).astype(np.uint8))
        img.save(loc)



init()