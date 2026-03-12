from fastapi import FastAPI

app = FastAPI(title="Meal Vision Service")


@app.post('/infer')
def infer(payload: dict) -> dict:
    return {
        'dish_name': 'grilled chicken with rice',
        'analysis_confidence': 0.74,
        'items': [
            {'name': 'chicken breast', 'grams': 160, 'confidence': 0.81},
            {'name': 'rice', 'grams': 120, 'confidence': 0.73},
        ],
    }
