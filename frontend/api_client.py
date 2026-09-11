import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def query_backend(question: str, image_bytes: bytes = None, image_name: str = "upload.jpg"):
    url = f"{API_BASE_URL}/query"
    
    # Multipart form data
    data = {"question": question}
    files = {}
    
    if image_bytes:
        files = {"image": (image_name, image_bytes, "image/jpeg")}
        
    try:
        response = requests.post(url, data=data, files=files if files else None)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {e}"}
