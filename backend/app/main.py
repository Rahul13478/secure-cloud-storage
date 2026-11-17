from fastapi import FastAPI
from app.routes import user , files , face_embadding, chain#importing 2 routers 
from app.routes.user import Lifespan

app = FastAPI(lifespan=Lifespan)
app.include_router(user.router)
app.include_router(files.router)
app.include_router(face_embadding.router)
app.include_router(chain.router)