from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app import models
from app.routes import category, product,auth
import logging




logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


logger.debug("Initializing database...")
Base.metadata.create_all(bind=engine)
logger.debug("Database initialized.")

app = FastAPI(title="Category & Product API")

logger.debug("Including routers...")
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)
logger.debug("Routers included.")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    logger.debug(f"Processing request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.debug(f"Request processed successfully: {request.method} {request.url}")
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )
@app.get("/")
def read_root():
    return {"message": "Category & Product API is running"}