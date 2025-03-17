from fastapi import APIRouter, Depends, HTTPException;
from lib.database.mysql import SessionLocal, GetDb, settings;
from typing import Annotated;
from lib.models.products import Product, NewProduct
from sqlalchemy.orm import Session;
from routers.auth import GetCurrentUser;
from starlette import status;
from lib.database.models import Products, Users;
from lib.helpers.auth import GenerateCode, AuthenticateUser, CreateAccessToken, GetCurrentUser, bcryptContext
from lib.models.users import User;
from sqlalchemy import select;

accountProductRouter = APIRouter(
    prefix="/account/products",
    tags=["profileProducts"]
)

dbDependency = Annotated[Session, Depends(GetDb)]
accountDependency = Annotated[dict, Depends(GetCurrentUser)]


@accountProductRouter.get("/{userId}", status_code=status.HTTP_200_OK)
async def GetProfileProducts(db: dbDependency, account: accountDependency):
    stmt = select(Products).where(account.userId == Products.userId)
    products = []
    for row in db.execute(stmt):
        products.append(Product(
            productId = row.productId,
            userId = row.userId,
            name = row.name,
            desc = row.desc,
            pricePlan = row.pricePlan,
            thumbnail = row.thumbnail
        ))
    return products

@accountProductRouter.get("/{productId}", status_code=status.HTTP_200_OK)
async def GetProduct(productId: int, db: dbDependency, account: accountDependency):
    product = db.query(Products).filter(Products.productId == productId).first()
    if product is None:
        raise HTTPException(status_code=401, detail="Error: Get Users Failed")
    return Product(
        productId = product.productId,
        userId = product.userId,
        name = product.name,
        desc = product.desc,
        pricePlan = product.pricePlan,
        thumbnail = product.thumbnail
    )

@accountProductRouter.post("/", status_code=status.HTTP_201_CREATED)
async def CreateProduct(account: accountDependency, db: dbDependency, formData: NewProduct):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    productModel = Products(
        userId = account.userId,
        name = formData.name,
        desc = formData.desc,
        pricePlan = formData.pricePlan,
        thumbnail = formData.thumbnail
    )
    db.add(productModel)
    db.commit()
    return formData

@accountProductRouter.put("/", status_code=status.HTTP_200_OK)
async def UpdateProduct(account: accountDependency, db: dbDependency, formData: Product):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    product = await db.query(Products).filter((Products.userId == account.userId) and (Products.productId == formData.productId)).first()
    if product is None:
        raise HTTPException(status_code=401, detail="Error: Update Products Failed")
    product.userId = formData.userId
    product.name = formData.name
    product.desc = formData.desc
    product.pricePlan = formData.pricePlan
    product.thumbnail = formData.thumbnail
    db.commit()
    db.refresh(product)
    return formData

@accountProductRouter.delete("/{productId}", status_code=status.HTTP_200_OK)
async def DeleteProduct(productId: int, db: dbDependency, account: accountDependency):
    db.query(Products).filter((Products.userId == account.userId) and (Products.productId == productId)).delete(synchronize_session=False)
    return 1
    