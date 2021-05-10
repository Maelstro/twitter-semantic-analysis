# main.py - main file of the application
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Create AGDS FastAPI instance
agds_api = FastAPI()

# Mount static and template directory
agds_api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@agds_api.get("/")
@agds_api.get("/hello")
async def hello():
    return "Hello World!"

@agds_api.post("/associate")
async def text_association(input_text: str) -> dict:
    return {}