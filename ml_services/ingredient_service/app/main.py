from fastapi import FastAPI

app = FastAPI(title="Ingredient Classification Service")


@app.post('/infer')
def infer(payload: dict) -> dict:
    return {'normalized_ingredients': payload.get('items', [])}
