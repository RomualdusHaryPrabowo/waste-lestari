import os
import logging
import tensorflow as tf
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance
_model = None
_class_names = [
    "battery",
    "biological",
    "cardboard",
    "clothes",
    "glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash",
]

CLASS_LABELS_INDONESIA = {
    "battery": "Baterai",
    "biological": "Biologis / Organik",
    "cardboard": "Karton",
    "clothes": "Pakaian",
    "glass": "Kaca",
    "metal": "Logam",
    "paper": "Kertas",
    "plastic": "Plastik",
    "shoes": "Sepatu",
    "trash": "Sampah Umum",
}

CLASS_COLORS = {
    "battery": "#e74c3c",
    "biological": "#27ae60",
    "cardboard": "#f39c12",
    "clothes": "#9b59b6",
    "glass": "#1abc9c",
    "metal": "#3498db",
    "paper": "#e67e22",
    "plastic": "#2ecc71",
    "shoes": "#8e44ad",
    "trash": "#7f8c8d",
}


def load_model(model_path=None):
    """Load the Keras MobileNetV2 model."""
    global _model

    if model_path is None:
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "..",
            "model",
            "ecosort_model.h5",
        )

    try:
        _model = tf.keras.models.load_model(model_path)
        logger.info(f"✅ Model berhasil dimuat dari: {model_path}")
    except Exception as e:
        logger.error(f"❌ Gagal memuat model: {e}")
        logger.info("🔄 Menggunakan model placeholder untuk development.")
        _model = None

    return _model


def get_model():
    if _model is None:
        load_model()
    return _model


def get_class_names():
    return _class_names


def predict_image(image, model=None):
    """
    Perform inference on a preprocessed image.
    Returns: (class_name, confidence, all_probabilities)
    """
    if model is None:
        model = get_model()

    if model is None:
        # Fallback: simulate prediction for development
        import random

        idx = random.randint(0, len(_class_names) - 1)
        all_probs = np.zeros(len(_class_names))
        all_probs[idx] = 0.85 + random.random() * 0.14
        for i in range(len(_class_names)):
            if i != idx:
                all_probs[i] = random.random() * 0.05
        all_probs /= all_probs.sum()
        return (
            _class_names[idx],
            float(np.max(all_probs)),
            all_probs.tolist(),
        )

    # Ensure correct input shape
    if len(image.shape) == 3:
        image = np.expand_dims(image, axis=0)

    predictions = model.predict(image, verbose=0)
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))

    return (
        _class_names[predicted_idx],
        confidence,
        predictions[0].tolist(),
    )