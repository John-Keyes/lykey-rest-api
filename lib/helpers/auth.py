import random
from datetime import datetime, timedelta, timezone
from typing import Annotated;
from fastapi import APIRouter, Depends, HTTPException, Body;
from lib.helpers.session import GetPair
from lib.helpers.mail import SendEmail
from pydantic import BaseModel;
from sqlalchemy.orm import Session;
from starlette import status;
from lib.database.mysql import settings;
from passlib.context import CryptContext;
from lib.database.models import Users;
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer;
from jose import jwt, JWTError;
from lib.models.auth import AuthLogin, Token, AuthVerify
from lib.models.users import User

bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto");
oauth2Bearer = OAuth2PasswordBearer(tokenUrl="/auth/session");

def GenerateCode(): 
    return str(random.randint(100000, 999999))
    

async def SendEmailCode(code: str, email: str):
    if settings.MODE != "dev":
        #Insert email code to person
        #verifyEndpoint = f"{settings.CLIENT_URL}/auth/verify"
        mailBody = {
            "email": email,
            "project_name": settings.MAIL_USERNAME,
            "url": f"{settings.CLIENT_URL}/auth/verify",
            "content": code
        }
        mailStatus = await SendEmail(
            subject="Email Verification: Registration Confirmation",
            emailTo=email, 
            body=mailBody, 
            template="email/email_verification.html"
        )
        return mailStatus
    print(f"Email sent to {email} with code: {code}.")
    

def VerifyEmailCode(userCode: str, formDataCode :str):
    if userCode != formDataCode:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Incorrect Code")
    # dev
    userCode = ""

def AuthenticateUser(email: str, formPassword: str, user: Users):
    if not user:
        return False
    if (email != user.email) or (not (bcryptContext.verify(formPassword, user.password))):
        return False
    return user

def CreateAccessToken(email: str, userId: int, expiresDelta):
    info = {"sub": email, "userId": userId}
    expires = datetime.now() + expiresDelta
    info.update({"exp": expires})
    return jwt.encode(info, settings.TOKEN_KEY, algorithm=settings.ALGORITHM)

async def GetCurrentUser():
    try:
        token = await GetPair("token")
        payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        userId: int = payload.get("userId")
        if email is None or userId is None:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Could not validate user")
        return {"email": email, "userId": userId}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error: Could not validate user")

async def GetSession(db, formData, user):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    authenticated = AuthenticateUser(formData.email, formData.password, user)
    if not authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error: Could not validate user")
    token = CreateAccessToken(user.email, user.userId, timedelta(minutes=20))
    return token