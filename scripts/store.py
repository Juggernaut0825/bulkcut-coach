import os
import json
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def _path(name):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, name)


def load(name, default=None):
    p = _path(name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return default if default is not None else {}


def save(name, data):
    with open(_path(name), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def today():
    return date.today().isoformat()


def get_today_log():
    logs = load('daily_logs.json', {})
    t = today()
    if t not in logs:
        logs[t] = {'meals': [], 'training': [], 'total_intake': 0, 'total_burned': 0}
    return logs, t


def save_meal(meal_data):
    logs, t = get_today_log()
    logs[t]['meals'].append(meal_data)
    logs[t]['total_intake'] = sum(m.get('calories', 0) for m in logs[t]['meals'])
    save('daily_logs.json', logs)


def save_training(training_data):
    logs, t = get_today_log()
    logs[t]['training'].append(training_data)
    logs[t]['total_burned'] = sum(tr.get('calories_burned', 0) for tr in logs[t]['training'])
    save('daily_logs.json', logs)
