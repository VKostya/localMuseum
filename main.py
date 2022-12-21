import uvicorn
from fastapi import FastAPI
from config import config
from web_api.base import api_router
import cloudinary

app = FastAPI()
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":

    uvicorn.run(app, host=config.HOST, port=config.PORT)
