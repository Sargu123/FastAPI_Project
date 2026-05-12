from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, SmallInteger, String, LargeBinary, Text
from sqlalchemy.orm import declarative_base
from database import Base


class Customer(Base):

      __tablename__ = "customers"

      customerNumber = Column(Integer, primary_key=True, index=True)

      customerName = Column(String(50), nullable=False)

      contactLastName = Column(String(50), nullable=False)

      contactFirstName = Column(String(50), nullable=False)

      phone = Column(String(50), nullable=False)

      addressLine1 = Column(String(50), nullable=False)

      addressLine2 = Column(String(50), nullable=True)

      city = Column(String(50), nullable=False)

      state = Column(String(50), nullable=True)

      postalCode = Column(String(15), nullable=True)

      country = Column(String(50), nullable=False)

      creditLimit = Column(Numeric(10, 2),nullable=True)
      salesRepEmployeeNumber: Column[int] = Column(Integer,ForeignKey("employees.employeeNumber"), nullable=True)


class Employee(Base):
    __tablename__ = "employees"

    employeeNumber: Column[int] = Column(Integer, primary_key=True,index=True)

    lastName = Column(String(50), nullable=False)

    firstName = Column(String(50), nullable=False)

    extension = Column(String(10), nullable=False)
    
    email = Column(String(100),nullable=False)

    officeCode = Column(String(100), nullable=False)

    reportsTo = Column(Integer,ForeignKey("employees.employeeNumber"),nullable=True)

    jobTitle = Column(String(50),nullable=False)


class ProductLine(Base):
      __tablename__ = "productlines"
      
      productLine = Column(String(50), primary_key=True, index=True)
      
      textDescription = Column(String(4000), nullable=True)
      
      htmlDescription = Column(String(4000), nullable=True)
      
      image = Column(String(300), nullable=True)

class Product(Base):
      __tablename__ = "products"
      productCode = Column(String(15), primary_key=True, index=True)
      productName = Column(String(70), nullable=False)
      productLine = Column(String(50), ForeignKey("productlines.productLine"), nullable=False)    
      productScale = Column(String(10), nullable=False)
      productVendor = Column(String(50), nullable=False)
      productDescription = Column(String(4000), nullable=False)
      quantityInStock = Column(Integer, nullable=False)
      buyPrice = Column(Numeric(10, 2), nullable=False)
      MSRP = Column(Numeric(10, 2), nullable=False)

class Office(Base):
    __tablename__ = "offices"

    officeCode = Column(String(10), primary_key=True, index=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50),nullable=False)
    addressLine1 = Column(String(50),nullable=False)
    addressLine2 = Column(String(50),nullable=True)
    state = Column(String(50),nullable=True)
    country = Column(String(50),nullable=False)
    postalCode = Column(String(15),nullable=False)
    territory = Column(String(10), nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"),primary_key=True,nullable=False)
    checkNumber = Column(String(50),primary_key=True,nullable=False)

    paymentDate = Column(Date,nullable=False)

    amount = Column(Numeric(10, 2),nullable=False)

class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True, index=True)

    orderDate = Column(Date, nullable=False)

    requiredDate = Column(Date, nullable=False)

    shippedDate = Column(Date, nullable=True)

    status = Column(String(15), nullable=False)
    comments = Column(Text, nullable=True)

    customerNumber = Column(
        Integer,
        ForeignKey("customers.customerNumber"),
        nullable=False
    )

class OrderDetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(
        Integer,
        ForeignKey("orders.orderNumber"),
        primary_key=True,
        nullable=False
    )

    productCode = Column(
        String(15),
        ForeignKey("products.productCode"),
        primary_key=True,
        nullable=False
    )

    quantityOrdered = Column(Integer, nullable=False)

    priceEach = Column(Numeric(10, 2), nullable=False)

    orderLineNumber = Column(SmallInteger, nullable=False)