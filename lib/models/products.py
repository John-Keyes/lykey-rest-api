from enum import Enum
from pydantic import BaseModel

class ProductPlan(Enum):
    FREE = 1
    MEMBER = 2
    PREMIUM = 3

class NewProduct(BaseModel):
    userId: int
    name: str
    desc: str
    pricePlan: ProductPlan
    thumbnail: str

class Product(NewProduct):
    productId: int