import json
from llm import chat
from store import save_training

PROMPT_TEMPLATE = """Estimate total calories burned for this workout session:
{workout}

Consider exercise type, sets, reps, weight, and typical energy expenditure.
Return ONLY valid JSON: {{"exercises": ["{name}", ...], "total_calories_burned": number}}"""


def log_training(exercises):
    """exercises: list of dicts with keys: name, sets, reps, weight_kg"""
    workout_text = '\n'.join(
        f"- {e['name']}: {e['sets']}x{e['reps']} @ {e['weight_kg']}kg"
        for e in exercises
    )
    raw = chat([{'role': 'user', 'content': PROMPT_TEMPLATE.format(workout=workout_text)}])
    raw = raw.strip().strip('`').removeprefix('json').strip()
    data = json.loads(raw)
    record = {
        'exercises': exercises,
        'calories_burned': data.get('total_calories_burned', 0),
    }
    save_training(record)
    return record
