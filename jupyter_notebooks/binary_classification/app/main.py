from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from predictor import ArchetypePredictor
from pydantic import BaseModel

class Tweet(BaseModel):
    text: str

# Initialize class with models
predictor = ArchetypePredictor()

# Initialize FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return "Hello, head to " \
           "/docs for API documentation, " \
           "/models/{archetype}/classify for checking if a given text applies a single archetype for a given text, or " \
           "/models/classify_all for classifying a text to all of the archetypes."

@app.post("/models/{archetype}/classify")
async def classify_archetype(archetype: str, text: Tweet):
    # Classify a Tweet to a single archetype
    global predictor
    (pred, prob_pred) = predictor.classify_to_archetype(text.text, archetype)

    # Convert the results to JSON
    item = {
        "text": text.text,
        f"{archetype}": {
            f"is_{archetype}": pred,
            "probability": prob_pred
        }
    }

    jsoned_item = jsonable_encoder(item)
    return JSONResponse(content=jsoned_item)

@app.post("/models/classify_all")
async def classify_all(text: Tweet):
    global predictor
    # Calculate response
    pred_out = predictor.classify_all(text.text)
    item = {
        "text": text.text,
        "predictions": pred_out
    }

    # Convert to JSON and return
    jsoned_item = jsonable_encoder(item)
    return JSONResponse(content=jsoned_item)