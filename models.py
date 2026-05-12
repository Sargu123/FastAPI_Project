from unicodedata import numeric
from datetime import date
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class Customer(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    creditLimit: Optional[float] = None
    salesRepEmployeeNumber: Optional[int] = None

class Employee(BaseModel):
    employeeNumber: int
    lastName: str
    firstName: str
    extension: str
    email: str
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str

class ProductLine(BaseModel):
    productLine: str
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    image: Optional[str] = None

class Product(BaseModel):
    productCode: str
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int
    buyPrice: float
    MSRP: float


class Office(BaseModel):
    officeCode: str
    city: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    state: Optional[str] = None
    country: str
    postalCode: str
    territory: str

class Payment(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: date
    amount: float

class Order(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

class OrderDetail(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: Decimal
    orderLineNumber: int