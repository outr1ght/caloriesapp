from fastapi import FastAPI

app = FastAPI(title="Portion Estimation Service")


@app.post('/infer')
def infer(payload: dict) -> dict:
    return {'portion_estimates': payload.get('items', [])}
