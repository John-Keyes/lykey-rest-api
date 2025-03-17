from datetime import timedelta, datetime;
from typing import Annotated;
from fastapi import APIRouter, Depends, HTTPException, Body;
from lib.helpers.session import StorePair, GetPair
from pydantic import BaseModel;
from sqlalchemy.orm import Session;
from starlette import status;
from sqlalchemy import select;
from lib.database.mysql import SessionLocal, GetDb, settings;
from lib.database.models import Users;
from lib.models.auth import *;
from lib.models.users import User;
from lib.helpers.auth import *;

authRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

dbDependency = Annotated[Session, Depends(GetDb)]

@authRouter.get("/session", status_code=status.HTTP_200_OK)
async def CheckSession(db: dbDependency, formData: AuthForgot):
    token = await GetPair(formData.email)
    if not token:
        return {"session": False, "role": Role.GUEST}
    return {"session": True, "role": Role.USER}

@authRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def Register(db: dbDependency, formData: AuthLogin):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    verificationCode = GenerateCode()
    authRegisterModel = Users(
        email=formData.email,
        password=bcryptContext.hash(formData.password),
        code = verificationCode,
        isVerified = 'F',
        country = "",
        pic = ""
    )
    db.add(authRegisterModel)
    db.commit()
    db.refresh(authRegisterModel)
    await SendEmailCode(verificationCode, formData.email)
    return {"email": formData.email}

@authRouter.put("/verify", status_code=status.HTTP_200_OK)
async def Verify(db: dbDependency, formData: AuthVerify):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    user = db.query(Users).filter(Users.email == formData.email).first()
    VerifyEmailCode(user.code, formData.code)
    token = await GetSession(db, formData, user)
    user.isVerified = 'T'
    user.role = Role.USER
    db.commit()
    db.refresh(user)
    #await StorePair(formData.email, token)
    return User(
        userId = user.userId,
        email = user.email,
        password = "",
        isVerified = 'T',
        role = Role.USER,
        country = user.country,
        pic = user.pic
    )

@authRouter.post("/login", status_code=status.HTTP_200_OK)
async def Login(db: dbDependency, formData: AuthLogin):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    stmt = select(Users).where(Users.email == formData.email).where(Users.isVerified == 'T')
    user = db.execute(stmt).first()
    token = await GetSession(db, formData, user)
    #await StorePair(formData.email, token)
    return User(
        userId = user.userId,
        email = user.email,
        password = "",
        isVerified = user.isVerified,
        role = user.role,
        country = user.country,
        pic = user.pic
    )

@authRouter.post("/password/forgot")
async def ForgotPwd(db: dbDependency, formData: AuthForgot):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    verificationCode = GenerateCode()
    user = db.query(Users).filter(Users.email == formData.email).first()
    user.code = verificationCode
    await SendEmailCode(verificationCode, user.email)
    db.commit()
    db.refresh(user)
    return {"email": formData.email}

@authRouter.put("/password/reset")
async def ResetPwd(db: dbDependency, formData: AuthVerify):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    user = db.query(Users).filter(Users.email == formData.email).first()
    VerifyEmailCode(user.code, formData.code)
    user.password = bcryptContext.hash(formData.password)
    db.commit()
    db.refresh(user)
    #await StorePair(formData.email, token)
    return User(
        userId = -1,
        email = "",
        password = "",
        isVerified = "",
        role = Role.GUEST,
        country = "",
        pic = ""
    )