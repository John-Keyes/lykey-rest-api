#from re import TEMPLATE
from fastapi import APIRouter, Depends, HTTPException;
from starlette import status;
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker
from pathlib import Path
from fastapi_mail.errors import ConnectionErrors
from lib.database.mysql import settings;

mailConfig = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_FROM_NAME=settings.DB_NAME,
    MAIL_PORT=int(settings.MAIL_PORT),
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

#TEMPLATE_FOLDER= Path(__file__).parent.parent/'templates/'

async def SendEmail(subject: str, emailTo: str, body: dict, template: str):
    message = MessageSchema(
        subject=subject,
        recipients= [emailTo,],
        template_body=body
    )
    fm = FastMail(mailConfig)
    try:
        await fm.send_message(message, template_name=template)
        return True
    except ConnectionErrors as e:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Could not validate user")
