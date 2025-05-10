# gemini_to_image.py
import google.generativeai as genai
import requests
import io
from PIL import Image

# ====== SET YOUR API KEYS ======
GEMINI_API_KEY = "AIzaSyBRRHCgiSBNbOOrcv0HG1UkF17Y6zxW-Do"
HUGGINGFACE_API_TOKEN = "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"

# ====== SETUP ======
genai.configure(api_key=GEMINI_API_KEY)
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
HF_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

# ====== USER INPUT ======
idea = input("What image would you like to generate? ")

# ====== GEMINI PROMPT ENGINEERING ======
prompt_request = f"""
Create a detailed, optimized prompt for generating an AI image based on this idea: '{idea}'.

The prompt should:
- Be specific about style, composition, lighting, colors, and mood
- Include relevant technical specifications (aspect ratio, quality level)
- Use descriptive language that AI image generators respond well to
- Be between 50-150 words

Return only the final prompt.
"""

# Generate image prompt with Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt_request)
image_prompt = response.text.strip()

print("\n🔷 Optimized Image Prompt:\n")
print(image_prompt)

# ====== IMAGE GENERATION ======
print("\n🎨 Generating image from Hugging Face API...")

response = requests.post(
    HF_API_URL,
    headers=headers,
    json={"inputs": image_prompt},
)

if response.status_code == 200:
    image = Image.open(io.BytesIO(response.content))
    image.save("generated_image.png")
    image.show()
    print("✅ Image saved as 'generated_image.png'")
else:
    print(f"❌ Error {response.status_code}:")
    print(response.text)
