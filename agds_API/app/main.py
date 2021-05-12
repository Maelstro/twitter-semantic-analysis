# main.py - main file of the application
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from text_processing.text_association import TextProcessor

# Create AGDS FastAPI instance
agds_api = FastAPI()

# Create TextProcessor instance
text_proc = TextProcessor()

# Mount static and template directory
agds_api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@agds_api.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@agds_api.get("/hello")
async def hello():
    return "Hello World!"

@agds_api.post("/associate", response_class=HTMLResponse)
async def text_association(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    # Calculate text similarity
    trait_result, influencer_list = text_proc.calculate_similarity(input_text)

    # Return trait outputs and list of ten most similar influencers
    return templates.TemplateResponse(name="process.html", context={
        "request": request,
        "input_text": input_text,
        "traits": trait_result.to_dict(),
        "most_similar_list": influencer_list.index[:10]
    })

@agds_api.post("/nn_associate", response_class=HTMLResponse)
async def nn_association(request: Request, input_text: str = Form(...)) -> templates.TemplateResponse:
    return templates.TemplateResponse(name="process.html", context={
        "request": request,
        "input_text": input_text,
        "traits": {}
    })