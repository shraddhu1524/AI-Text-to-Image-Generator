
import os
import uuid
import base64
from pathlib import Path

import requests
from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

# Configure image storage
IMAGE_DIR = BASE_DIR / "static" / "generated"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Cloudflare credentials
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

# Cloudflare AI model
MODEL_NAME = "@cf/black-forest-labs/flux-1-schnell"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_image():

    try:
        # Get user prompt
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt", "").strip()

        # Validate prompt
        if not prompt:
            return jsonify({
                "error": "Please enter an image description."
            }), 400

        if len(prompt) > 1000:
            return jsonify({
                "error": "Prompt must be under 1000 characters."
            }), 400

        # Check Cloudflare credentials
        if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
            return jsonify({
                "error": "Cloudflare credentials are missing. Check your .env file."
            }), 500

        # Cloudflare API endpoint
        api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL_NAME}"
        )

        # Send prompt to Cloudflare
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"prompt": prompt},
            timeout=180
        )

        # Log API errors
        if response.status_code != 200:
            app.logger.error(
                "Cloudflare status: %s",
                response.status_code
            )
            app.logger.error(
                "Cloudflare response: %s",
                response.text
            )

        # Stop if API request failed
        response.raise_for_status()

        # Read Cloudflare response
        result = response.json()

        # Get generated image
        image_base64 = result.get("result", {}).get("image")

        if not image_base64:
            raise RuntimeError(
                "Cloudflare did not return an image."
            )

        # Decode Base64 image
        image_bytes = base64.b64decode(image_base64)

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.png"
        image_path = IMAGE_DIR / filename

        # Save generated image
        image_path.write_bytes(image_bytes)

        # Create image URL
        image_url = url_for(
            "static",
            filename=f"generated/{filename}"
        )

        return jsonify({
            "success": True,
            "image_url": image_url,
            "message": "Image generated successfully!"
        })

    except requests.exceptions.HTTPError as error:
        app.logger.exception("Cloudflare HTTP error")
        return jsonify({
            "error": "Cloudflare API error. Check the VS Code terminal for details."
        }), 502

    except requests.exceptions.RequestException:
        app.logger.exception("Cloudflare connection error")
        return jsonify({
            "error": "Could not connect to Cloudflare. Check your internet connection."
        }), 502

    except Exception:
        app.logger.exception("Image generation failed")
        return jsonify({
            "error": "Image generation failed. Check the VS Code terminal for details."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
