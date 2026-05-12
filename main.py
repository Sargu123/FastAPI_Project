from fastapi import Depends, FastAPI
from sqlalchemy import select
import database
import database_models
from models import Customer, Employee, ProductLine, Product, Office, Payment,  Order, OrderDetail
from database import AsyncSessionLocal, get_db, init_models
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from logger import get_logger

logger = get_logger("fastapi-app")

logger.info("Logger is working - INFO")
logger.warning("Logger is working - WARNING")
logger.error("Logger is working - ERROR")


#creating FastAPI

#base is the parent class for all SQLAlchemy models.
#create tables in PostgreSQL, equivalent to running SQL like CREATE TABLE customers
#bind= engine, connects SQLAlchemy to the PostgreSQL database specified in database.py

@asynccontextmanager
async def lifespan(app: FastAPI):

    # startup
    await init_models()

    yield

    # shutdown (optional cleanup here)

app = FastAPI(lifespan=lifespan)


#End point 1 for home page
@app.get("/")
def greet():
    return "hello world"

#adding value to the database, table name customers
customers = [
   Customer(
        customerNumber=103,
        customerName="Atelier graphique",
        contactLastName="Schmitt",
        contactFirstName="Carine",
        phone="40.32.2555",
        addressLine1="54, rue Royale",
        addressLine2=None,
        city="Nantes",
        state=None,
        postalCode="44000",
        country="France",
        creditLimit=21000.00,
        salesRepEmployeeNumber="1370"
    ),

    Customer(
        customerNumber=112,
        customerName="Signal Gift Stores",
        contactLastName="Parker",
        contactFirstName="Peter",
        phone="986252997",
        addressLine1="New York",
        addressLine2=None,
        city="New York City",
        state=None,
        postalCode="53739",
        country="USA",
        creditLimit=20000,
        salesRepEmployeeNumber="1166"
    )
    
]



#end point 2 for customers
@app.get("/customers")

async def get_all_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(database_models.Customer)
    )
    return result.scalars().all()

#end point for getting customer by id
@app.get("/customers/{customer_id}")
async def read_customer_by_id(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await crud.get_customer_by_id(db, customer_id)

#endpoint for creating a new customer
@app.post("/customers")
async def create_customer(
    customer: Customer,
    db: AsyncSession = Depends(get_db)
):

    db.add(database_models.Customer(**customer.model_dump()))

    await db.commit()

    return {"message": "Customer created successfully"}

#endpoint for updating a customer by id

@app.put("/customers/{customer_id}")
async def update_customer(
    customer_id: int,
    customer: Customer,
    db: AsyncSession = Depends(get_db)
):

    return await crud.update_customer_by_id(db, customer_id, customer)

#endpoint for deleting a customer by id
@app.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await crud.delete_customer_by_id(db, customer_id)

#adding value to the database, table name employees

employees = [

     Employee(
        employeeNumber=1002,
        lastName="Murphy",
        firstName="Diane",
        extension="x5800",
        email="dmurphy@classicmodelcars.com",
        officeCode="1",
        reportsTo=None,
        jobTitle="President"
    ),

    Employee(
        employeeNumber=1056,
        lastName="Patterson",
        firstName="Mary",
        extension="x4611",
        email="mpatterso@classicmodelcars.com",
        officeCode="1",
        reportsTo=1002,
        jobTitle="VP Sales"
    ),

    Employee(
        employeeNumber=1076,
        lastName="Firrelli",
        firstName="Jeff",
        extension="x9273",
        email="jfirrelli@classicmodelcars.com",
        officeCode="1",
        reportsTo=1002,
        jobTitle="VP Marketing"
    ),

    Employee(
        employeeNumber=1088,
        lastName="Patterson",
        firstName="William",
        extension="x4871",
        email="wpatterson@classicmodelcars.com",
        officeCode="6",
        reportsTo=1056,
        jobTitle="Sales Manager (APAC)"
    ),

    Employee(
        employeeNumber=1102,
        lastName="Bondur",
        firstName="Gerard",
        extension="x5408",
        email="gbondur@classicmodelcars.com",
        officeCode="4",
        reportsTo=1056,
        jobTitle="Sale Manager (EMEA)"
    ),

    Employee(
        employeeNumber=1143,
        lastName="Bow",
        firstName="Anthony",
        extension="x5428",
        email="abow@classicmodelcars.com",
        officeCode="1",
        reportsTo=1056,
        jobTitle="Sales Manager (NA)"
    )

]

#end point for getting all employees

@app.get("/employees")
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(database_models.Employee)
    )
    return result.scalars().all()

#end point for getting employee by id

@app.get("/employees/{employee_id}")
async def get_employee_by_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_employee_by_id(db, employee_id)

#end point for creating a new employee

@app.post("/employees")
async def create_employee(
    employee: Employee,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_employee(db, employee)

#end point for updating an employee by id

@app.put("/employees/{employee_id}")
async def update_employee_by_id(
    employee_id: int,
    updated_employee: Employee,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_employee_by_id(db, employee_id, updated_employee)

#end point for deleting an employee

@app.delete("/employees/{employee_id}")
async def delete_employee_by_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_employee_by_id(db, employee_id)

#end point for getting all product lines

#end point for getting productlines
@app.get("/productlines")
async def get_all_productlines(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_productlines(db)

#end point for creating a new product line

@app.post("/productlines")
async def create_productline(
    productline: ProductLine,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_productline(db, productline)

#end point for updating a product line by id
@app.put("/productlines/{productline_id}")
async def update_productline_by_id(
    productline_id: str,
    updated_productline: ProductLine,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_productline_by_id(db, productline_id, updated_productline)

#end point for deleting a product line
@app.delete("/productlines/{productline_id}")
async def delete_productline_by_id(
    productline_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_productline_by_id(db, productline_id)

#endpoint for getting all the product
@app.get("/products")
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_products(db)

#endpoint for getting product by id
@app.get("/products/{product_id}")
async def get_product_by_id(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_product_by_id(db, product_id)

#endpoint for creating a new product
@app.post("/products")
async def create_product(
    product: Product,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(db, product)

# updating a product by product id
@app.put("/products/{product_id}")
async def update_product_by_code(
    product_code: str,
    updated_product: Product,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_product_by_code(db, product_code, updated_product)

#end point deleting a product by product code

@app.delete("/products/{product_code}")

async def delete_product_by_code(
    product_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_product_by_code(db, product_code)

#end point for getting all products

@app.get("/offices")
async def get_all_offices(db: AsyncSession = Depends(get_db)):
   return await crud.get_all_offices(db)

#end point for getting office by office code

@app.get("/offices/{office_code}")
async def get_office_by_code(office_code: str,db: AsyncSession = Depends(get_db)):

    return await crud.get_office_by_code(db, office_code)

#endpoint for creating a new office
@app.post("/offices")
async def create_office(office: Office, db: AsyncSession = Depends(get_db)):

    return await crud.create_office(db, office)

#endpoint for updating office by office code

@app.put("/offices/{office_code}")
async def update_office_by_code(
    office_code: str,
    updated_office: Office,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_office_by_code(db, office_code, updated_office)

#endpoint for deleting a office by code
@app.delete("/offices/{office_code}")
async def delete_office_by_code(
    office_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_office_by_code(db, office_code)

#end point for getting all payments

@app.get("/payments")
async def get_all_payments(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_payments(db)


#end point for getting payment by customer number and check number
@app.post("/payments/{customer_number}/{check_number}")
async def create_payment(
    customer_number: int,
    check_number: str,
    payment: Payment,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_payment(db, payment)

#end point for deleting a payment by customer number and check number
@app.delete("/payments/{customer_number}/{check_number}")
async def delete_payment_by_id(
    customer_number: int,
    check_number: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_payment_by_id(db, customer_number, check_number)

#end point for updating a payment by customer number and check number

@app.put("/payments/{customer_number}/{check_number}")
async def update_payment_by_id(
    customer_number: int,
    check_number: str,
    updated_payment: Payment,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_payment_by_id(
        db,
        customer_number,
        check_number,
        updated_payment
    )

#end point for getting all the orders
@app.get("/orders")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_orders(db)

#end point for getting order by id
@app.get("/orders/{orderNumber}")
async def get_order_by_id(
    orderNumber: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_order_by_id(db, orderNumber)


#end point for updating order by id
@app.put("/orders/{orderNumber}")
async def update_order_by_id(
    orderNumber: int,
    updated_order: Order,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_order_by_id(
        db,
        orderNumber,
        updated_order
    )

#end point for deleting a order
@app.delete("/orders/{orderNumber}")
async def delete_order_by_id(
    orderNumber: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_order_by_id(db, orderNumber)

#end point for getting all the order details

@app.get("/orderdetails")
async def get_all_order_details(
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_order_details(db)

#end point for getting order details by id
@app.get("/orderdetails/{order_number}/{product_code}")
async def get_order_detail_by_id(
    order_number: int,
    product_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_order_detail_by_id(
        db,
        order_number,
        product_code
    )

#end point for deleting a order detail

@app.delete("/orderdetails/{order_number}/{product_code}")
async def delete_order_detail(
    order_number: int,
    product_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.delete_order_detail_by_id(
        db,
        order_number,
        product_code
    )

#end point for updating order details

@app.put("/orderdetails/{order_number}/{product_code}")
async def update_order_detail(
    order_number: int,
    product_code: str,
    updated_data: OrderDetail,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_order_detail(
        db,
        order_number,
        product_code,
        updated_data
    )