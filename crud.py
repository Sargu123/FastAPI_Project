from sqlite3 import IntegrityError
import database_models
from models import Customer, Employee, ProductLine, Product, Office, Payment, Order, OrderDetail
from database import AsyncSessionLocal, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



# -----------------------------
# INIT CUSTOMERS
# -----------------------------
# =====================================================
# INIT CUSTOMERS
# =====================================================

async def init_customers(
    db: AsyncSession,
    customers: list
):

    result = await db.execute(
        select(Customer)
    )

    existing_customer = result.scalars().first()

    if not existing_customer:

        db.add_all([
            Customer(**c.model_dump())
            for c in customers
        ])

        await db.commit()

        print("Customers seeded successfully")

    else:
        print("Customers already exist, skipping...")


# -----------------------------
# INIT EMPLOYEES
# -----------------------------

async def init_employees(
    db: AsyncSession,
    employees: list
):

    result = await db.execute(
        select(Employee)
    )

    existing_employee = result.scalars().first()

    if not existing_employee:

        db.add_all([
            Employee(**e.model_dump())
            for e in employees
        ])

        await db.commit()

        print("Employees seeded successfully")

    else:
        print("Employees already exist, skipping...")

async def init_productlines(
    db: AsyncSession,
    productlines: list
):

    result = await db.execute(
        select(database_models.ProductLine)
    )

    existing = result.scalars().first()

    if not existing:

        db.add_all([
            database_models.ProductLine(
                **p.model_dump()
            )
            for p in productlines
        ])

        await db.commit()

        print("ProductLines seeded successfully")

    else:
        print("ProductLines already exist")

# -----------------------------
# MASTER INIT FUNCTION
# -----------------------------
async def init_models():
    async with AsyncSessionLocal() as db:
        await init_customers(db, Customer)
        await init_employees(db, Employee)
        await init_productlines(db, ProductLine)




# Get all customers
async def get_all_customers(
    db: AsyncSession
):

    result = await db.execute(
        select(database_models.Customer)
    )

    return result.scalars().all()

# Get all customers by their id
async def get_customer_by_id(
    db: AsyncSession,
    customer_id: int
):

    result = await db.execute(
        select(database_models.Customer).where(
            database_models.Customer.customerNumber == customer_id
        )
    )

    return result.scalars().first()

# post customer 
async def create_customer(db: AsyncSession, customer: Customer):

    try:
        new_customer = database_models.Customer(**customer.model_dump())

        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)

        return {
            "customerNumber": new_customer.customerNumber,
            "customerName": new_customer.customerName
        }

    except Exception as e:
        await db.rollback()
        raise e

#putting a customer by id

async def update_customer_by_id(
    db: AsyncSession,
    customer_id: int,
    updated_customer
):

    try:
        # 1. Find existing customer
        result = await db.execute(
            select(database_models.Customer).where(
                database_models.Customer.customerNumber == customer_id
            )
        )

        db_customer = result.scalars().first()

        # 2. If not found
        if not db_customer:
            return {
                "status": "error",
                "message": "Customer not found"
            }

        # 3. Update fields (exclude primary key)
        for key, value in updated_customer.model_dump(
            exclude={"customerNumber"}
        ).items():
            setattr(db_customer, key, value)

        # 4. Commit changes
        await db.commit()
        await db.refresh(db_customer)

        return {
            "status": "success",
            "data": {
                "customerNumber": db_customer.customerNumber,
                "customerName": db_customer.customerName,
                "city": db_customer.city,
                "country": db_customer.country
            }
        }

    # 5. Handle DB errors safely
    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    
#delete customer by id
async def delete_customer_by_id(
    db: AsyncSession,
    customer_id: int
):
    try:
        result = await db.execute(
            select(database_models.Customer).where(
                database_models.Customer.customerNumber == customer_id
            )
        )
        db_customer = result.scalars().first()

        if not db_customer:
            return {
                "status": "error",
                "message": "Customer not found"
            }

        await db.delete(db_customer)
        await db.commit()

        return {
            "status": "success",
            "message": "Customer deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }


# function for getting all employees
async def get_all_employees(db: AsyncSession):
    result = await db.execute(
        select(database_models.Employee)
    )
    return result.scalars().all()

#function for getting employee by id

async def get_employee_by_id(db: AsyncSession, employee_id: int):

    result = await db.execute(
        select(database_models.Employee).where(
            database_models.Employee.employeeNumber == employee_id
        )
    )

    return result.scalars().first()

#function for creating a new employee
async def create_employee(db: AsyncSession, employee: Employee):
    try:
        new_employee = database_models.Employee(**employee.model_dump())

        db.add(new_employee)
        await db.commit()
        await db.refresh(new_employee)

        return {
            "employeeNumber": new_employee.employeeNumber,
            "firstName": new_employee.firstName,
            "lastName": new_employee.lastName
        }

    except Exception as e:
        await db.rollback()
        raise e
    
#function for updating an employee by id
async def update_employee_by_id(
    db: AsyncSession,
    employee_id: int,
    updated_employee
):

    try:
        result = await db.execute(
            select(database_models.Employee).where(
                database_models.Employee.employeeNumber == employee_id
            )
        )

        db_employee = result.scalars().first()

        if not db_employee:
            return {
                "status": "error",
                "message": "Employee not found"
            }

        for key, value in updated_employee.model_dump(
            exclude={"employeeNumber"}
        ).items():
            setattr(db_employee, key, value)

        await db.commit()
        await db.refresh(db_employee)

        return {
            "status": "success",
            "data": {
                "employeeNumber": db_employee.employeeNumber,
                "firstName": db_employee.firstName,
                "lastName": db_employee.lastName,
                "jobTitle": db_employee.jobTitle
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for deleting an employee

async def delete_employee_by_id(
    db: AsyncSession,
    employee_id: int
):
    try:
        result = await db.execute(
            select(database_models.Employee).where(
                database_models.Employee.employeeNumber == employee_id
            )
        )
        db_employee = result.scalars().first()

        if not db_employee:
            return {
                "status": "error",
                "message": "Employee not found"
            }

        await db.delete(db_employee)
        await db.commit()

        return {
            "status": "success",
            "message": "Employee deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting all the productlines
async def get_all_productlines(db: AsyncSession):
    result = await db.execute(
        select(database_models.ProductLine)
    )
    return result.scalars().all()

#function for posting a new productline

async def create_productline(db: AsyncSession, productline: ProductLine):
    try:
        new_productline = database_models.ProductLine(**productline.model_dump())

        db.add(new_productline)
        await db.commit()
        await db.refresh(new_productline)

        return {
            "productLine": new_productline.productLine,
            "textDescription": new_productline.textDescription
        }

    except Exception as e:
        await db.rollback()
        raise e

#function for updating a productline by id

async def update_productline_by_id(
    db: AsyncSession,
    productline_id: str,
    updated_productline: ProductLine
):
    try:
        result = await db.execute(
            select(database_models.ProductLine).where(
                database_models.ProductLine.productLine == productline_id
            )
        )

        db_productline = result.scalars().first()

        if not db_productline:
            return {
                "status": "error",
                "message": "Product line not found"
            }

        for key, value in updated_productline.model_dump(
            exclude={"productLine"}
        ).items():
            setattr(db_productline, key, value)

        await db.commit()
        await db.refresh(db_productline)

        return {
            "status": "success",
            "data": {
                "productLine": db_productline.productLine,
                "textDescription": db_productline.textDescription
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for deleting a productline by id
async def delete_productline_by_id(db: AsyncSession, productline_id: str):
    try:
        result = await db.execute(
            select(database_models.ProductLine).where(
                database_models.ProductLine.productLine == productline_id
            )
        )
        db_productline = result.scalars().first()

        if not db_productline:
            return {
                "status": "error",
                "message": "Product line not found"
            }

        await db.delete(db_productline)
        await db.commit()

        return {
            "status": "success",
            "message": "Product line deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

# function for getting all products
async def get_all_products(db: AsyncSession):
    result = await db.execute(
        select(database_models.Product)
    )
    return result.scalars().all()

# function for getting a product by id

async def get_product_by_id(db: AsyncSession, product_id: str):
    result = await db.execute(
        select(database_models.Product).where(
            database_models.Product.productCode == product_id
        )
    )

    return result.scalars().first()

#function for creating a new product
async def create_product(db: AsyncSession, product: Product):
    try:
        new_product = database_models.Product(**product.model_dump())

        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)

        return {
            "productCode": new_product.productCode,
            "productName": new_product.productName
        }

    except Exception as e:
        await db.rollback()
        raise e
    
#function for updating a product by id
async def update_product_by_code(db: AsyncSession, product_code: str, updated_product: Product):
    try:
        result = await db.execute(
            select(database_models.Product).where(
                database_models.Product.productCode == product_code
            )
        )

        db_product = result.scalars().first()

        if not db_product:
            return {
                "status": "error",
                "message": "Product not found"
            }

        for key, value in updated_product.model_dump(
            exclude={"productCode"}
        ).items():
            setattr(db_product, key, value)

        await db.commit()
        await db.refresh(db_product)

        return {
            "status": "success",
            "data": {
                "productCode": db_product.productCode,
                "productName": db_product.productName,
                "productLine": db_product.productLine,
                "buyprice": db_product.buyPrice
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for deleting a product by id
async def delete_product_by_code(db: AsyncSession, product_code: str):
    try:
        result = await db.execute(
            select(database_models.Product).where(
                database_models.Product.productCode == product_code
            )
        )
        db_product = result.scalars().first()

        if not db_product:
            return {
                "status": "error",
                "message": "Product not found"
            }

        await db.delete(db_product)
        await db.commit()

        return {
            "status": "success",
            "message": "Product deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    
#function for getting list of all offices
async def get_all_offices(db: AsyncSession):
    result = await db.execute(
        select(database_models.Office)
    )
    return result.scalars().all()

#function for getting list of all offices by Office code
async def get_office_by_code(db: AsyncSession, office_code: str):
    result = await db.execute(
        select(database_models.Office).where(
            database_models.Office.officeCode == office_code
        )
    )

    return result.scalars().first()

#function for creating a new office
async def create_office(db:AsyncSession, office: Office):
    try:
        new_office = database_models.Office(**office.model_dump())

        db.add(new_office)
        await db.commit()
        await db.refresh(new_office)

        return {
            "officeCode": new_office.officeCode,
            "city": new_office.city
        }

    except Exception as e:
        await db.rollback()
        raise e
    
#function for updating an office by id

async def update_office_by_code(db: AsyncSession, office_code: str, updated_office: Office):
    try:
        result = await db.execute(
            select(database_models.Office).where(
                database_models.Office.officeCode == office_code
            )
        )

        db_office = result.scalars().first()

        if not db_office:
            return {
                "status": "error",
                "message": "Office not found"
            }

        for key, value in updated_office.model_dump(
            exclude={"officeCode"}
        ).items():
            setattr(db_office, key, value)

        await db.commit()
        await db.refresh(db_office)

        return {
            "status": "success",
            "data": {
                "officeCode": db_office.officeCode,
                "city": db_office.city,
                "country": db_office.country
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for deleting an office by id
async def delete_office_by_code(db: AsyncSession, office_code: str):
    try:
        result = await db.execute(
            select(database_models.Office).where(
                database_models.Office.officeCode == office_code
            )
        )
        db_office = result.scalars().first()

        if not db_office:
            return {
                "status": "error",
                "message": "Office not found"
            }

        await db.delete(db_office)
        await db.commit()

        return {
            "status": "success",
            "message": "Office deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting list of all payments


async def get_all_payments(db: AsyncSession):
    result = await db.execute(
        select(database_models.Payment)
    )

    return result.scalars().all()

#function for creating payments
async def create_payment(db: AsyncSession, payment: Payment):
    try:
        new_payment = database_models.Payment(**payment.model_dump())

        db.add(new_payment)
        await db.commit()
        await db.refresh(new_payment)

        return {
            "customerNumber": new_payment.customerNumber,
            "checkNumber": new_payment.checkNumber
        }

    except Exception as e:
        await db.rollback()
        raise e


        
#function for deleting a payment by id
async def delete_payment_by_id(db: AsyncSession, customer_number: int, check_number: str):
    try:
        result = await db.execute(
            select(database_models.Payment).where(
                database_models.Payment.customerNumber == customer_number,
                database_models.Payment.checkNumber == check_number
            )
        )
        db_payment = result.scalars().first()

        if not db_payment:
            return {
                "status": "error",
                "message": "Payment not found"
            }

        await db.delete(db_payment)
        await db.commit()

        return {
            "status": "success",
            "message": "Payment deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    


#updating payment by id
async def update_payment_by_id(db: AsyncSession, customer_number: int, check_number: str, updated_payment: Payment):
    try:
        result = await db.execute(
            select(database_models.Payment).where(
                database_models.Payment.customerNumber == customer_number,
                database_models.Payment.checkNumber == check_number
            )
        )

        db_payment = result.scalars().first()

        if not db_payment:
            return {
                "status": "error",
                "message": "Payment not found"
            }

        for key, value in updated_payment.model_dump(
            exclude={"customerNumber", "checkNumber"}
        ).items():
            setattr(db_payment, key, value)

        await db.commit()
        await db.refresh(db_payment)

        return {
            "status": "success",
            "data": {
                "customerNumber": db_payment.customerNumber,
                "checkNumber": db_payment.checkNumber,
                "amount": db_payment.amount
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting all orders
async def get_all_orders(db: AsyncSession):
    try:
        result = await db.execute(
            select(database_models.Order)
        )

        orders = result.scalars().all()

        return {
            "status": "success",
            "data": orders
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting orders by order id
async def get_order_by_id(db: AsyncSession, orderNumber: int):
    try:
        result = await db.execute(
            select(database_models.Order).where(
                database_models.Order.orderNumber == orderNumber
            )
        )

        order = result.scalars().first()

        if not order:
            return {
                "status": "error",
                "message": "Order not found"
            }

        return {
            "status": "success",
            "data": order
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

#function for updating order by id
async def update_order_by_id(db: AsyncSession, orderNumber: int, updated_order: Order):
    try:
        result = await db.execute(
            select(database_models.Order).where(
                database_models.Order.orderNumber == orderNumber
            )
        )

        db_order = result.scalars().first()

        if not db_order:
            return {
                "status": "error",
                "message": "Order not found"
            }

        for key, value in updated_order.model_dump(
            exclude={"orderNumber"}
        ).items():
            setattr(db_order, key, value)

        await db.commit()
        await db.refresh(db_order)

        return {
            "status": "success",
            "data": {
                "orderNumber": db_order.orderNumber,
                "orderDate": db_order.orderDate,
                "requiredDate": db_order.requiredDate,
                "shippedDate": db_order.shippedDate,
                "status": db_order.status,
                "comments": db_order.comments,
                "customerNumber": db_order.customerNumber
            }
        }

    except IntegrityError:
        await db.rollback()
        return {
            "status": "error",
            "message": "Database integrity error"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }


#function for deleting a order

async def delete_order_by_id(db: AsyncSession, orderNumber: int):
    try:
        result = await db.execute(
            select(database_models.Order).where(
                database_models.Order.orderNumber == orderNumber
            )
        )
        db_order = result.scalars().first()

        if not db_order:
            return {
                "status": "error",
                "message": "Order not found"
            }

        await db.delete(db_order)
        await db.commit()

        return {
            "status": "success",
            "message": "Order deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting all the order details
async def get_all_order_details(db: AsyncSession):
    try:
        result = await db.execute(
            select(database_models.OrderDetail)
        )

        order_details = result.scalars().all()

        return {
            "status": "success",
            "data": order_details
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

#function for getting order details by order number
async def get_order_detail_by_id(
    db: AsyncSession,
    order_number: int,
    product_code: str
):
    try:
        result = await db.execute(
            select(database_models.OrderDetail).where(
                database_models.OrderDetail.orderNumber == order_number,
                database_models.OrderDetail.productCode == product_code
            )
        )

        order_detail = result.scalars().first()

        if not order_detail:
            return {
                "status": "error",
                "message": "Order detail not found"
            }

        return {
            "status": "success",
            "data": {
                "orderNumber": order_detail.orderNumber,
                "productCode": order_detail.productCode,
                "quantityOrdered": order_detail.quantityOrdered,
                "priceEach": float(order_detail.priceEach),
                "orderLineNumber": order_detail.orderLineNumber
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

#function for deleting a orderdetail by id
async def delete_order_detail_by_id(
    db: AsyncSession,
    order_number: int,
    product_code: str
):
    try:
        result = await db.execute(
            select(database_models.OrderDetail).where(
                database_models.OrderDetail.orderNumber == order_number,
                database_models.OrderDetail.productCode == product_code
            )
        )

        order_detail = result.scalars().first()

        if not order_detail:
            return {
                "status": "error",
                "message": "Order detail not found"
            }

        await db.delete(order_detail)
        await db.commit()

        return {
            "status": "success",
            "message": "Order detail deleted successfully"
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    
#updating order details by id

async def update_order_detail(
    db: AsyncSession,
    order_number: int,
    product_code: str,
    updated_data: OrderDetail
):
    try:
        result = await db.execute(
            select(database_models.OrderDetail).where(
                database_models.OrderDetail.orderNumber == order_number,
                database_models.OrderDetail.productCode == product_code
            )
        )

        db_order_detail = result.scalars().first()

        if not db_order_detail:
            return {
                "status": "error",
                "message": "Order detail not found"
            }

        # update fields except primary keys
        for key, value in updated_data.model_dump(
            exclude={"orderNumber", "productCode"}
        ).items():
            setattr(db_order_detail, key, value)

        await db.commit()
        await db.refresh(db_order_detail)

        return {
            "status": "success",
            "data": {
                "orderNumber": db_order_detail.orderNumber,
                "productCode": db_order_detail.productCode,
                "quantityOrdered": db_order_detail.quantityOrdered,
                "priceEach": float(db_order_detail.priceEach),
                "orderLineNumber": db_order_detail.orderLineNumber
            }
        }

    except Exception as e:
        await db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }