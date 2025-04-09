import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from .routers import promotion, resources
#from .dependencies.populate_data import populate_data

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

# Includes the new routers

app.include_router(promotion.router)


app.include_router(resources.router)


if __name__ == "__main__":
    populate_data()
    print("Data population called")
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)