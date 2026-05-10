import numpy as np
from PIL import Image
import tensorflow as tf


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for MobileNetV2 inference.
    - Resize to 224x224
    - Convert to array
    - Apply MobileNetV2 preprocessing
    - Return numpy array ready for model
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size, Image.Resampling.LANCZOS)

    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)

    # MobileNetV2 preprocessing
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    return img_array