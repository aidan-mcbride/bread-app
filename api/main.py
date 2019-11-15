from fastapi import FastAPI

from api.routers import auth, recipes, users

app = FastAPI(
    title="Bread App API",
    description="https://github.com/aidan-mcbride/bread-app",
    version="1",
)
# https://fastapi.tiangolo.com/tutorial/application-configuration/


# @app.get("/")
# async def read_main() -> dict:
#     return {"msg": "Hello World"}


"""
import routers
see: https://fastapi.tiangolo.com/tutorial/bigger-applications/#the-main-fastapi
"""

app.include_router(auth.router, tags=["authentication"])
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(users.router, prefix="/users", tags=["users"])
