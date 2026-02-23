import os
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL = 'google/gemini-3-flash-preview'
URL = 'https://openrouter.ai/api/v1/chat/completions'


def chat(messages, max_tokens=2048):
    resp = requests.post(URL, headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }, json={'model': MODEL, 'messages': messages, 'max_tokens': max_tokens})
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def chat_with_image(image_path, prompt):
    with open(image_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(image_path)[1].lower().strip('.')
    mime = f'image/{"jpeg" if ext in ("jpg","jpeg") else ext}'
    messages = [{'role': 'user', 'content': [
        {'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{b64}'}},
        {'type': 'text', 'text': prompt},
    ]}]
    return chat(messages)
