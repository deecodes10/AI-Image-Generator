# 🎨 AI Image Studio

AI Image Studio is a web-based AI image generation application built with Python and Streamlit. It allows users to turn text prompts into AI-generated images using the Hugging Face FLUX.1-schnell model.

## ✨ Features

- 📝 Generate images from natural-language prompts
- 🎨 Choose from multiple image styles
- 🖼️ Generate 1–4 images from a prompt
- ⬇️ Download generated images
- 📜 View generation history during the current session
- 🌸 Clean pastel-themed user interface
- 🔐 Secure Hugging Face API key management using environment variables

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Hugging Face Inference API**
- **FLUX.1-schnell**
- **Pillow**
- **python-dotenv**

## ⚙️ How It Works

```text
User Prompt
     ↓
Style Selection
     ↓
Prompt + Style
     ↓
Hugging Face Inference API
     ↓
FLUX.1-schnell
     ↓
AI Generated Image
     ↓
Display + Download + History