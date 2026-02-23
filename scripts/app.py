import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from food import analyze_photo, analyze_text
from training import log_training
from metabolism import set_metrics, get_profile
from store import get_today_log, load, save
from llm import chat


def cmd_photo(path):
    print(f'Analyzing {path}...')
    result = analyze_photo(path)
    print(f"\nCalories: {result['calories']} kcal")
    print(f"Protein: {result['protein_g']}g | Carbs: {result['carbs_g']}g | Fat: {result['fat_g']}g")
    for it in result['items']:
        print(f"  - {it['food']}: {it['calories']} kcal")


def cmd_meal(desc):
    print(f'Estimating: {desc}...')
    result = analyze_text(desc)
    print(f"\nCalories: {result['calories']} kcal")
    print(f"Protein: {result['protein_g']}g | Carbs: {result['carbs_g']}g | Fat: {result['fat_g']}g")


def cmd_train():
    exercises = []
    print('Log exercises (empty name to finish):')
    while True:
        name = input('  Exercise: ').strip()
        if not name:
            break
        sets = int(input('  Sets: '))
        reps = int(input('  Reps: '))
        weight = float(input('  Weight (kg): '))
        exercises.append({'name': name, 'sets': sets, 'reps': reps, 'weight_kg': weight})
    if exercises:
        result = log_training(exercises)
        print(f"\nEstimated burn: {result['calories_burned']} kcal")


def cmd_metrics():
    h = float(input('Height (cm): '))
    w = float(input('Weight (kg): '))
    a = int(input('Age: '))
    g = input('Gender (male/female): ').strip().lower()
    bf = input('Body fat % (optional, press enter to skip): ').strip()
    bf = float(bf) if bf else None
    p = set_metrics(h, w, a, g, bf)
    print(f"\nBMR: {p['bmr']} kcal/day")
    print(f"TDEE: {p['tdee']} kcal/day")


def cmd_summary():
    logs, t = get_today_log()
    day = logs[t]
    profile = get_profile()
    tdee = profile.get('tdee', 0)
    target = load('goal.json', {}).get('target_calories', tdee)
    print(f"\n=== {t} Summary ===")
    print(f"Intake:  {day['total_intake']} kcal ({len(day['meals'])} meals)")
    print(f"Burned:  {day['total_burned']} kcal ({len(day['training'])} sessions)")
    print(f"TDEE:    {tdee} kcal")
    print(f"Target:  {target} kcal")
    net = day['total_intake'] - day['total_burned'] - tdee
    print(f"Balance: {net:+d} kcal")


def cmd_goal(goal_type):
    profile = get_profile()
    tdee = profile.get('tdee', 2000)
    multipliers = {'cut': 0.8, 'bulk': 1.15, 'maintain': 1.0}
    m = multipliers.get(goal_type, 1.0)
    target = round(tdee * m)
    save('goal.json', {'goal': goal_type, 'target_calories': target})
    print(f"Goal: {goal_type} | Target: {target} kcal/day")


def cmd_plan():
    profile = get_profile()
    goal = load('goal.json', {})
    logs, t = get_today_log()
    context = json.dumps({'profile': profile, 'goal': goal, 'today': logs.get(t, {})}, indent=2)
    prompt = f"""Based on this user data, generate a concise weekly training and diet plan.
{context}
Include: daily calorie/macro targets, meal suggestions, workout split. Be specific and practical."""
    print('Generating plan...\n')
    print(chat([{'role': 'user', 'content': prompt}]))


def main():
    if len(sys.argv) < 2:
        print('Usage: python app.py <command> [args]')
        print('Commands: photo, meal, train, metrics, summary, goal, plan, history')
        return
    cmd = sys.argv[1]
    if cmd == 'photo' and len(sys.argv) > 2:
        cmd_photo(sys.argv[2])
    elif cmd == 'meal' and len(sys.argv) > 2:
        cmd_meal(' '.join(sys.argv[2:]))
    elif cmd == 'train':
        cmd_train()
    elif cmd == 'metrics':
        cmd_metrics()
    elif cmd == 'summary':
        cmd_summary()
    elif cmd == 'goal' and len(sys.argv) > 2:
        cmd_goal(sys.argv[2])
    elif cmd == 'plan':
        cmd_plan()
    elif cmd == 'history':
        logs = load('daily_logs.json', {})
        for d in sorted(logs.keys(), reverse=True)[:7]:
            day = logs[d]
            print(f"{d}: intake={day['total_intake']}kcal burned={day['total_burned']}kcal")
    else:
        print(f'Unknown command or missing args: {cmd}')


if __name__ == '__main__':
    main()
