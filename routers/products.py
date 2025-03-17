from fastapi import APIRouter, Depends, HTTPException;
from lib.database.mysql import SessionLocal, GetDb, settings;
from typing import Annotated;
from sqlalchemy.orm import Session;
from routers.auth import GetCurrentUser;
from starlette import status;
from lib.database.models import Products, Users;
from sqlalchemy import select;
from lib.models.products import Product;

productRouter = APIRouter(
    prefix="/products",
    tags=["products"]
)

dbDependency = Annotated[Session, Depends(GetDb)]

@productRouter.get("/", status_code=status.HTTP_200_OK)
async def GetProducts(db: dbDependency):
    stmt = select(Products)
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

@productRouter.get("/{productId}", status_code=status.HTTP_200_OK)
async def GetProduct(productId: int, db: dbDependency):
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