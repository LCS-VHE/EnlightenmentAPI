"""
A list of useful functions that the api would use
"""
import os
import time
import numpy as np
import tensorflow_hub as hub
from PIL import Image
from joblib import load
from tensorflow import keras
import tensorflow as tf
from constants import PLACEHOLDING_DATA_DIR, IMAGES_DIR

"""
A list of global variables
"""
autoencoder = keras.models.load_model(os.path.join(os.curdir, "Models", "Best Model.h5"),
                                      custom_objects={"rounded_accuracy": lambda x: x})
decoder = autoencoder.layers[1]
pca = load(os.path.join(os.curdir, "Models", 'Trained .joblib'))
neural_style_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

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
    if not loc:  # With no defined path
        img = []
        filename = f"Anime Face{time.time()}.png"  # The format of the anime face
        for index in range(len(sliders)):
            img.append(sliders[index] / 10 * (maxs[index] - mins[index]))

        img = pca.inverse_transform([img])
        img = decoder.predict(img).reshape((64, 64, 3))

        img = np.clip(img, 0, 1)
        img = Image.fromarray((img * 255).astype(np.uint8))
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

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1

    tensor = tensor[0]
    return Image.fromarray(tensor)

def save_neural_style_model(original_image, style_image):
    """

    :param original_image: A directory to the original image
    :param style_image: The directory to the style image
    :return: filename of the saved image
    """
    global neural_style_model
    style_image = load_img(style_image)
    original_image = load_img(original_image)
    styled_image = neural_style_model(tf.constant(original_image), tf.constant(style_image))[0]

    filename = f"{time.time()}.jpeg"
    tensor_to_image(styled_image).save(os.path.join(IMAGES_DIR, filename))
    return filename
def get_filename_from_neural_transfer_link():
    filename = ""
    return filename

init()
