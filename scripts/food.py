import json
from llm import chat, chat_with_image
from store import save_meal

PROMPT = """Analyze this food image. Estimate calories and macros.
Return ONLY valid JSON: {"food": "name", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number}
If multiple items, return a JSON array. Be realistic with portions shown."""


def analyze_photo(image_path):
    raw = chat_with_image(image_path, PROMPT)
    raw = raw.strip().strip('`').removeprefix('json').strip()
    data = json.loads(raw)
    items = data if isinstance(data, list) else [data]
    total = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0, 'items': items}
    for it in items:
        for k in ('calories', 'protein_g', 'carbs_g', 'fat_g'):
            total[k] += it.get(k, 0)
    save_meal(total)
    return total


def analyze_text(description):
    prompt = f"""Estimate calories and macros for: {description}
Return ONLY valid JSON: {{"food": "name", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number}}"""
    raw = chat([{'role': 'user', 'content': prompt}])
    raw = raw.strip().strip('`').removeprefix('json').strip()
    data = json.loads(raw)
    items = data if isinstance(data, list) else [data]
    total = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0, 'items': items}
    for it in items:
        for k in ('calories', 'protein_g', 'carbs_g', 'fat_g'):
            total[k] += it.get(k, 0)
    save_meal(total)
    return total
