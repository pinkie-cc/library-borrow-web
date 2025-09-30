from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.openapi.utils import get_openapi

from models.user import User
from config.database import engine, Base
from core.exception_handlers import http_exception_handler
from core.oauth2 import get_current_user

from routes import auth, category, book, borrow

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database initialization with schemas and connecting engines
Base.metadata.create_all(bind=engine)

# Custom exception handler registration. it will get HTTPException and return a custom JSON response.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path,
        },
    )
# app.add_exception_handler(HTTPException, http_exception_handler)

# Include routers for different modules with a common prefix
app.include_router(auth.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(book.router, prefix="/api")
app.include_router(borrow.router, prefix="/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="Custom JWT Bearer Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root(current_user: User = Depends(get_current_user)):
    return {"message": "Library Management!"}

# run the following code only when this file is executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True, port=8000)