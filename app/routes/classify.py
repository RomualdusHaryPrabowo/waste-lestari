import os
import uuid
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename

from app.models.model_loader import predict_image
from app.utils.preprocessing import preprocess_image
from app.models.model_loader import CLASS_LABELS_INDONESIA, CLASS_COLORS

classify_bp = Blueprint("classify", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@classify_bp.route("/")
def classify_page():
    return render_template("classify.html")


@classify_bp.route("/api/predict", methods=["POST"])
def api_predict():
    if "image" not in request.files:
        return jsonify({"error": "Tidak ada gambar yang dikirim"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Nama file kosong"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Format file tidak didukung"}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    upload_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "..", "uploads"
    )
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_name)
    file.save(filepath)

    try:
        # Preprocess
        preprocessed = preprocess_image(filepath)

        # Predict
        class_name, confidence, all_probs = predict_image(preprocessed)

        # Get label in Indonesian
        label = CLASS_LABELS_INDONESIA.get(class_name, class_name)
        color = CLASS_COLORS.get(class_name, "#2ecc71")

        # Build top-3 results
        indexed_probs = list(enumerate(all_probs))
        indexed_probs.sort(key=lambda x: x[1], reverse=True)
        top3 = []
        for idx, prob in indexed_probs[:3]:
            top3.append(
                {
                    "class": CLASS_LABELS_INDONESIA.get(
                        class_name, class_name
                    ),
                    "confidence": round(float(prob) * 100, 2),
                }
            )

        result = {
            "success": True,
            "prediction": label,
            "class_key": class_name,
            "confidence": round(confidence * 100, 2),
            "color": color,
            "top3": top3,
            "image_url": f"/uploads/{unique_name}",
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500