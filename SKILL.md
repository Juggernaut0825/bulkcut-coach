---
name: bulkcut-coach
description: Fitness and diet tracking tool. Use when the user wants to analyze food photos for calories, log workouts, calculate metabolism (BMR/TDEE), get daily calorie summaries, or generate training/diet plans. Invoked with /bulkcut-coach.
user-invocable: true
license: MIT
---

# BulkCut Coach - Fitness & Diet Tracker

A CLI fitness tool that uses Gemini 3 Flash (via OpenRouter) for food photo analysis and personalized planning.

## Capabilities

1. **Food Photo Analysis** - Analyze food images to estimate calories and macros (protein/carbs/fat)
2. **Training Log** - Log exercises with sets/reps/weight, estimate calories burned
3. **Body Metrics** - Calculate BMR/TDEE from height/weight/age/body fat
4. **Daily Summary** - Show calorie balance (intake vs expenditure vs target)
5. **Plan Generation** - Create personalized training and diet plans based on goals

## Setup

Requires:
- Python 3.10+
- `pip install -r requirements.txt`
- `.env` file with `OPENROUTER_API_KEY=<your-key>`

## Usage

```bash
python scripts/app.py <command> [args]
```

### Commands
- `photo <image_path>` - Analyze a food photo
- `meal <description>` - Log a meal by text description
- `train` - Log a training session interactively
- `metrics` - Set/update body metrics
- `summary` - Show today's calorie summary
- `plan` - Generate a training/diet plan
- `goal <cut|bulk|maintain>` - Set your training goal
- `history` - View recent logs

## Technical Details

- LLM: `google/gemini-3-flash-preview` via OpenRouter
- API key from `.env` as `OPENROUTER_API_KEY`
- Data stored in `data/` directory as JSON files
- Food analysis uses multimodal (image + text) prompts
