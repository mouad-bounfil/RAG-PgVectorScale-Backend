from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.agents import agents_bp

app = Flask(__name__, static_folder="views", static_url_path="")
CORS(app)

load_dotenv()


@app.route("/")
def index():
    """Serve the main chat interface"""
    return send_from_directory("views", "index.html")


if __name__ == "__main__":
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.run(port=8080, debug=True)
