from store import load, save

PROFILE_FILE = 'profile.json'


def set_metrics(height_cm, weight_kg, age, gender, body_fat_pct=None):
    profile = load(PROFILE_FILE, {})
    profile.update(height_cm=height_cm, weight_kg=weight_kg, age=age,
                   gender=gender, body_fat_pct=body_fat_pct)
    profile['bmr'] = calc_bmr(profile)
    profile['tdee'] = calc_tdee(profile)
    save(PROFILE_FILE, profile)
    return profile


def calc_bmr(p):
    if p.get('body_fat_pct'):
        lbm = p['weight_kg'] * (1 - p['body_fat_pct'] / 100)
        return round(370 + 21.6 * lbm)  # Katch-McArdle
    if p['gender'] == 'male':
        return round(10 * p['weight_kg'] + 6.25 * p['height_cm'] - 5 * p['age'] + 5)
    return round(10 * p['weight_kg'] + 6.25 * p['height_cm'] - 5 * p['age'] - 161)


def calc_tdee(p, activity_factor=1.55):
    return round(p['bmr'] * activity_factor)


def get_profile():
    return load(PROFILE_FILE, {})
