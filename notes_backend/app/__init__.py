from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS for public preview
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI/Swagger configuration
app.config["API_TITLE"] = "Notes API - Ocean Professional"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)

# Basic error handlers to keep envelope consistent
@app.errorhandler(404)
def handle_404(e):
    return jsonify({"status": "error", "data": None, "message": "Resource not found"}), 404


@app.errorhandler(400)
def handle_400(e):
    return jsonify({"status": "error", "data": None, "message": "Bad request"}), 400


@app.errorhandler(500)
def handle_500(e):
    return jsonify({"status": "error", "data": None, "message": "Internal server error"}), 500
