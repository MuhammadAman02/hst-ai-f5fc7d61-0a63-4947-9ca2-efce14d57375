from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Configure Jinja2 templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def hello_world(request: Request):
    """Render the Hello World page."""
    return templates.TemplateResponse("hello_world.html", {"request": request})

# Add additional frontend routes here using the @router decorator