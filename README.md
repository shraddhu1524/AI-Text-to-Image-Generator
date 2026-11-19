# AI Text-to-Image Generator 🎨

An AI-powered web application that transforms text prompts into images using generative AI. Users can enter a prompt and generate unique images through a simple and interactive web interface.

## ✨ Features

- Generate images from text prompts
- Simple and user-friendly interface
- AI-powered image generation using FLUX
- Flask backend for handling requests
- Generated images displayed on the web interface

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Cloudflare Workers AI
- FLUX (`@cf/black-forest-labs/flux-1-schnell`)

## 📂 Project Structure

```text
I_Text_To_Image_Generator/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── generated/
├── requirements.txt
└── .env (not uploaded)
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/shraddhu1524/AI-Text-to-Image-Generator.git
cd AI-Text-to-Image-Generator
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
```

Replace the placeholders with your own Cloudflare credentials.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5001
```

## 🔐 Security

API credentials are stored in environment variables and should never be committed to GitHub.

## 👩‍💻 Author

Shraddha

---

If you like this project, feel free to explore the repository!
