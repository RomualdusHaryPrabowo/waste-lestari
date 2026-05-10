import os
from flask import Flask


def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ecosort-ai-secret-2026")
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "..", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Blueprints
    from app.routes.main import main_bp
    from app.routes.classify import classify_bp
    from app.routes.education import education_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(classify_bp, url_prefix="/classify")
    app.register_blueprint(education_bp, url_prefix="/education")

    return app