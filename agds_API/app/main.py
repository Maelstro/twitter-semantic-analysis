# main.py - main file of the application
from fastapi import FastAPI, Request
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

@agds_api.get("/")
@agds_api.get("/hello")
async def hello():
    return "Hello World!"

@agds_api.post("/associate")
async def text_association(input_text: str) -> dict:
    # Calculate text similarity
    trait_result, influencer_list = text_proc.calculate_similarity(input_text)

    # Parse the results - get 10 most similar influencers

    return {
        "traits": trait_result.to_dict(),
        "most_similar_list": influencer_list.index[:10]
    }