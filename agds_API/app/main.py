# main.py - main file of the application
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from text_processing.text_association import TextProcessor
from starlette.exceptions import HTTPException as StarletteHTTPException
import asyncio
import json
import aioredis
import pandas as pd

redis = aioredis.from_url("redis://agds-redis")

# Create AGDS FastAPI instance
agds_api = FastAPI()

# Create TextProcessor instance
text_proc = TextProcessor()

# Mount static and template directory
agds_api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@agds_api.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    x = await redis.keys('prefix:*')
    for key in x: redis.delete(key)
    return templates.TemplateResponse(name="index.html", context={"request": request})

@agds_api.get("/hello")
async def hello():
    return "Hello World!"

@agds_api.post("/associate", response_class=HTMLResponse)
async def text_association(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    # Calculate text similarity
    trait_result, influencer_list = text_proc.calculate_similarity(input_text)
    trait_result = trait_result.to_dict()
    await redis.set("agds_traits", json.dumps(trait_result))
    await redis.set("agds_most_similar", json.dumps(influencer_list.to_dict()))

    # Neural network processing
    text_pred = text_proc.predict_nn(input_text)
    nn_similarity = text_proc.nn_similarity(text_pred)
    text_pred = text_pred.to_dict()

    await redis.set("nn_traits", json.dumps(text_pred))
    await redis.set("nn_most_similar", json.dumps(nn_similarity.to_dict()))

    # Return trait outputs and list of ten most similar influencers
    return templates.TemplateResponse(name="process.html", context={
        "request": request,
        "input_text": input_text,
        "traits": trait_result,
        "most_similar_list": influencer_list[:10],
        "model_type": "AGDS"
    })

@agds_api.post("/nn_associate", response_class=HTMLResponse)
async def nn_association(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    trait_result = await redis.get("nn_traits")
    influencer_list = await redis.get("nn_most_similar")
    influencer_list = pd.Series(json.loads(influencer_list))

    return templates.TemplateResponse(name="process.html", context={
        "request": request,
        "input_text": input_text,
        "traits": json.loads(trait_result),
        "most_similar_list": influencer_list[:10],
        "model_type": "LSTM"
    })

@agds_api.post("/agds_associate", response_class=HTMLResponse)
async def agds_association(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    trait_result = await redis.get("agds_traits")
    influencer_list = await redis.get("agds_most_similar")
    influencer_list = pd.Series(json.loads(influencer_list))

    return templates.TemplateResponse(name="process.html", context={
        "request": request,
        "input_text": input_text,
        "traits": json.loads(trait_result),
        "most_similar_list": influencer_list[:10],
        "model_type": "AGDS"
    })

@agds_api.post("/compare", response_class=HTMLResponse)
async def compare_results(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    agds_trait_result = await redis.get("agds_traits")
    agds_influencer_list = await redis.get("agds_most_similar")
    agds_influencer_list = json.loads(agds_influencer_list)

    nn_trait_result = await redis.get("nn_traits")
    nn_influencer_list = await redis.get("nn_most_similar")
    nn_influencer_list = json.loads(nn_influencer_list)

    # Create lists
    l_inf = [agds_influencer_list, nn_influencer_list]
    l_tr = [json.loads(agds_trait_result), json.loads(nn_trait_result)]

    both_influencer_list = list(zip(*map(dict.items, l_inf)))
    both_traits = list(zip(*map(dict.items, l_tr)))

    return templates.TemplateResponse(name="compare.html", context={
        "request": request,
        "input_text": input_text,
        "both_traits": both_traits,
        "both_most_similar_list": both_influencer_list[:10],
    })


@agds_api.exception_handler(StarletteHTTPException)
async def http_exception(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(name="40X.html", context={
        "request": request,
    }, status_code=exc.status_code)

@agds_api.on_event("shutdown")
async def shutdown_event():
    redis.close()