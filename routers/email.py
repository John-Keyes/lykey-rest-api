from fastapi import APIRouter, Depends, HTTPException;
from starlette import status;
from lib.database.mysql import SessionLocal, GetDb, settings;
from lib.models.users import User
from lib.models.email import Email
from lib.helpers.auth import *

emailRouter = APIRouter(
    prefix="/email"
)

@emailRouter.post("/", status_code=status.HTTP_201_CREATED)
async def Contact(formData: Email):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    mailBody = {
        "email": formData.email,
        "project_name": settings.MAIL_USERNAME,
        "message": formData.message,
        "subject": formData.subject
    }
    mailStatus = await SendEmail(
        subject=formData.subject,
        emailTo=formData.email, 
        body=mailBody, 
        template="email"
    )
    return mailStatus