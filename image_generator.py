import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Find the .env file in the same folder as this Python file
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Get Hugging Face token
token = os.getenv("HF_TOKEN")

# Check whether token was loaded
print("Token loaded:", bool(token))

if not token:
    raise ValueError("HF_TOKEN was not found. Check your .env file.")

# Create Hugging Face client
client = InferenceClient(
    provider="nscale",
    api_key=token
)

# Generate image
image = client.text_to_image(
    prompt="A cute robot sitting in a coffee shop, cinematic lighting, highly detailed",
    model="black-forest-labs/FLUX.1-schnell"
)

# Save image
image.save("test_image.png")

print("Image generated successfully!")
print("Saved as test_image.png")