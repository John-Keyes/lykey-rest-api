from lib.database.mysql import Base
from lib.models.auth import Role
from lib.models.products import ProductPlan
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Text, Integer, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.types import Enum

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "sfs1", "mysql_engine":"InnoDB", "mysql_collate":"utf8mb4_unicode_ci"} 
    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True)
    password = Column(String(256), unique=True)
    code = Column(String(6), nullable=True)
    isVerified = Column(String(1), nullable=True)
    role = Column(Enum(Role, native_enum=False), default=Role.GUEST, nullable=False)
    country = Column(String(50), nullable=True)
    pic = Column(Text, nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

class Products(Base):
    __tablename__ = "Products"
    __table_args__ = {"schema": "sfs1", "mysql_engine":"InnoDB", "mysql_collate":"utf8mb4_unicode_ci"}
    productId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    desc = Column(Text, nullable=True)
    pricePlan = Column(Enum(ProductPlan, native_enum=False), default=ProductPlan.FREE, nullable=False)
    thumbnail = Column(Text, nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())