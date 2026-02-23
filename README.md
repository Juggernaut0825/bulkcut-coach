# BulkCut Coach

AI-powered fitness & diet tracking skill for Claude Code. Snap a photo of your meal, log your workout, and get personalized plans — all through natural conversation.

## Features

- **Food Photo Analysis** — Send a food photo, get calorie & macro estimates (protein/carbs/fat) powered by Gemini 3 Flash vision
- **Text Meal Logging** — Describe what you ate in plain text, get nutritional breakdown
- **Workout Logging** — Log exercises with sets, reps, and weight to estimate calories burned
- **Body Metrics & Metabolism** — Input height, weight, age, body fat % to calculate BMR and TDEE
- **Goal Setting** — Set your goal (cut / bulk / maintain) and get a daily calorie target
- **Daily Summary** — See your calorie balance: intake vs expenditure vs target
- **AI Training & Diet Plans** — Generate personalized weekly plans based on your data and goals

## Install

```bash
npx skills add Juggernaut0825/bulkcut-coach
```

Then add your OpenRouter API key to the project `.env`:

```
OPENROUTER_API_KEY=<your-key>
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Once installed, just talk to Claude naturally:

- *"Analyze this food photo"* + attach image
- *"I ate two eggs, rice, and chicken breast for lunch"*
- *"I did 4x4 back squat at 112.5kg and 3x2 power cleans at 67.5kg"*
- *"Set my metrics: 178cm, 80kg, 28 years old, male, 15% body fat"*
- *"What's my calorie summary today?"*
- *"Generate a training plan for cutting"*

## Tech Stack

- **LLM**: Gemini 3 Flash (`google/gemini-3-flash-preview`) via OpenRouter
- **Language**: Python 3.10+
- **Data**: Local JSON storage in `data/`

## License

MIT
