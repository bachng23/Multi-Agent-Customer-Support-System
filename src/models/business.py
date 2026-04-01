from __future__ import annotations
from src.models.base import BaseModel
from sqlmodel import SQLModel, create_engine, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.models.support import SupportTicket


class Customer(BaseModel, table=True):
    full_name: str = Field(..., description="The full name of the customer") 
    email: str = Field(..., description="The email address of the customer", unique=True, index=True)
    phone_number: Optional[str] = Field(None, description="The phone number of the customer")
    
    tickets: list[SupportTicket] = Relationship(back_populates="customer")
    orders: list["Order"] = Relationship(back_populates="customer")

class Order(BaseModel, table=True):
    order_id: str = Field(..., description="The unique identifier for the order", unique=True, index=True)
    total_amount: float = Field(..., description="The total amount of the order", ge=0)
    status: str = Field(..., description="The status of the order", default="pending")
    customer_id: uuid.UUID = Field(foreign_key="customer.id")

    customer: Customer = Relationship(back_populates="orders")

    items: list["OrderItem"] = Relationship(back_populates="order")

class Product(BaseModel, table=True):
    name: str = Field(..., description="The name of the product")
    sku: str = Field(..., description="The stock keeping unit of the product", unique=True)
    description: Optional[str] = Field(None, description="The description of the product")
    price: float = Field(..., description="The price of the product", ge=0)
    category: Optional[str] = Field(None, description="The category of the product")

    order_items: list["OrderItem"] = Relationship(back_populates="product")

class OrderItem(BaseModel, table=True):
    order_id: uuid.UUID = Field(foreign_key="order.id", primary_key=True)
    product_id: uuid.UUID = Field(foreign_key="product.id", primary_key=True)
    quantity: int = Field(default=1)
    unit_price: float = Field(default=0.0, description="The price of a single unit of the product at the time of the order", ge=0)

    order: Order = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="order_items")


