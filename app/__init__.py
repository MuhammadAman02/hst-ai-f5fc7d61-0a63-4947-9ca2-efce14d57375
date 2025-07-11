import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import core components
from .core.config import settings
from .core.logging_config import get_logger
from .core.error_handling import register_exception_handlers

# Initialize main application logger
logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-ready FastAPI application base.",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: Static directory not found at {static_dir}")

# Configure Jinja2 templates
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    templates = None
    print(f"Warning: Templates directory not found at {templates_dir}")

# Import and include routers
from .api import routes as api_routes
from .frontend import routes as frontend_routes

# Include routers
app.include_router(api_routes.router, prefix="/api", tags=["api"])
app.include_router(frontend_routes.router, tags=["frontend"])

# Register custom exception handlers
register_exception_handlers(app)

# --- Startup and Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV})")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")