from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from lib.database import mysql
from lib.database.mysql import SessionLocal, engine
from routers.auth import authRouter
from routers.users import userRouter
from routers.email import emailRouter
from routers.account import accountRouter
from routers.products import productRouter
from routers.account.products import accountProductRouter
from lib.helpers.config import Settings, GetSettings

api = FastAPI()
api.include_router(authRouter)
api.include_router(userRouter)
api.include_router(emailRouter)
api.include_router(productRouter)
api.include_router(accountRouter)
api.include_router(accountProductRouter)

mysql.Base.metadata.create_all(bind=engine)

@api.get("/")
async def Info(settings: Annotated[Settings, Depends(GetSettings)]):
    return {
        "MODE": settings.MODE,
        "DB_HOST": settings.DB_HOST,
        "DB_USER": settings.DB_USER,
        "DB_PWD": settings.DB_PWD,
        "DB_ROOT_PWD": settings.DB_ROOT_PWD,
        "DB_PORT": settings.DB_PORT,
        "EXTRA_DB_PORT": settings.EXTRA_DB_PORT,
        "DB_NAME": settings.DB_HOST,
        "API_PORT": settings.API_PORT,
        "CLIENT_PORT": settings.CLIENT_PORT,
        "CLIENT_URL": settings.CLIENT_URL,
        "API_URL": settings.API_URL,
        "TOKEN_KEY": settings.TOKEN_KEY,
        "REDIS_URL": settings.REDIS_URL,
        "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY,
        "AWS_REGION": settings.AWS_REGION,
        "BUCKET_NAME": settings.BUCKET_NAME,
        "DB_URL": settings.DB_URL,
        "MAIL_USERNAME": settings.MAIL_USERNAME,
        "MAIL_PASSWORD": settings.MAIL_PASSWORD,
        "MAIL_FROM": settings.MAIL_FROM,
        "MAIL_PORT": settings.MAIL_PORT,
        "MAIL_SERVER": settings.MAIL_SERVER
    }