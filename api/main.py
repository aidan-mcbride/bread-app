from fastapi import FastAPI

from api.routers import recipes

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


"""
import routers
see: https://fastapi.tiangolo.com/tutorial/bigger-applications/#the-main-fastapi
"""

app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
