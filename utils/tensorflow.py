import tensorflow as tf
from PIL import Image
import numpy as np

def preprocess(image):
    im = Image.open(image)
    im = im.resize((224, 224))
    im_final = im.convert("RGB")
    x = tf.keras.preprocessing.image.img_to_array(im_final)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    return x