# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Customer(Base):
    """
    description: Customers with personal data, balance, and credit limit.
    """
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    credit_limit = Column(Float, default=1000.0, nullable=False)

class Order(Base):
    """
    description: Orders made by customers, including a notes field.
    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    notes = Column(String, nullable=True)
    amount_total = Column(Float, default=0.0, nullable=False)

class Product(Base):
    """
    description: Products available for purchase with detailed information.
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, default=0.0, nullable=False)

class OrderItem(Base):
    """
    description: Items within an order, linking products and orders together.
    """
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, default=0.0, nullable=False)

class Inventory(Base):
    """
    description: Inventory details for products including stock levels.
    """
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    stock = Column(Integer, default=0, nullable=False)

class Supplier(Base):
    """
    description: Suppliers providing products to be sold.
    """
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)

class SupplierProduct(Base):
    """
    description: Relationship between suppliers and products they provide.
    """
    __tablename__ = 'supplier_products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

class Shipment(Base):
    """
    description: Shipments related to orders for delivery purposes.
    """
    __tablename__ = 'shipments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    shipment_date = Column(DateTime, nullable=True)

class Category(Base):
    """
    description: Categories to categorize different products.
    """
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class ProductCategory(Base):
    """
    description: Many-to-many relationship between products and categories.
    """
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

class Payment(Base):
    """
    description: Payment information linked to orders.
    """
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, default=0.0, nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now, nullable=False)

class Review(Base):
    """
    description: Customer reviews of products.
    """
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    review_text = Column(String, nullable=True)
    rating = Column(Integer, default=0, nullable=False)

# Create the tables
Base.metadata.create_all(engine)

# Adding sample data
# Create customers
customers = [
    Customer(name='John Doe', balance=500.0, credit_limit=1500.0),
    Customer(name='Jane Smith', balance=250.0, credit_limit=1000.0),
    Customer(name='Alice Johnson', balance=300.0, credit_limit=1200.0),
    Customer(name='Emily Davis', balance=0.0, credit_limit=2000.0),
    Customer(name='Michael Brown', balance=450.0, credit_limit=1300.0)
]

# Create products
products = [
    Product(name='Laptop', price=1000.0),
    Product(name='Smartphone', price=600.0),
    Product(name='Tablet', price=400.0),
    Product(name='Headphones', price=150.0),
    Product(name='Monitor', price=300.0)
]

# Create orders
orders = [
    Order(customer_id=1, notes="Urgent delivery", amount_total=1600.0),
    Order(customer_id=2, notes="Include gift wrap", amount_total=450.0),
    Order(customer_id=3, notes="Set up required", amount_total=700.0),
    Order(customer_id=5, notes="Deliver to work address", amount_total=1200.0),
    Order(customer_id=4, notes="Delayed payment", amount_total=240.0)
]

# Create order items
order_items = [
    OrderItem(order_id=1, product_id=1, quantity=1, price=1000.0),
    OrderItem(order_id=1, product_id=4, quantity=4, price=150.0),
    OrderItem(order_id=2, product_id=2, quantity=1, price=600.0),
    OrderItem(order_id=2, product_id=3, quantity=2, price=300.0),
    OrderItem(order_id=3, product_id=5, quantity=1, price=300.0),
    OrderItem(order_id=4, product_id=1, quantity=1, price=1000.0),
    OrderItem(order_id=5, product_id=3, quantity=1, price=400.0)
]

# Create inventory
inventory = [
    Inventory(product_id=1, stock=50),
    Inventory(product_id=2, stock=30),
    Inventory(product_id=3, stock=20),
    Inventory(product_id=4, stock=100),
    Inventory(product_id=5, stock=40)
]

# Create suppliers
suppliers = [
    Supplier(name='Tech Supplies Co', contact_info='info@techsupplies.com'),
    Supplier(name='Gadget Provisioners', contact_info='sales@gadgets.com'),
    Supplier(name='Digital Devices Ltd', contact_info='support@digitaldevices.com')
]

# Create supplier products
supplier_products = [
    SupplierProduct(supplier_id=1, product_id=1),
    SupplierProduct(supplier_id=1, product_id=2),
    SupplierProduct(supplier_id=2, product_id=3),
    SupplierProduct(supplier_id=2, product_id=4),
    SupplierProduct(supplier_id=3, product_id=5)
]

# Create shipments
shipments = [
    Shipment(order_id=1, shipment_date=datetime.datetime.now()),
    Shipment(order_id=2, shipment_date=datetime.datetime.now() + datetime.timedelta(days=2)),
    Shipment(order_id=3, shipment_date=datetime.datetime.now() + datetime.timedelta(days=1)),
    Shipment(order_id=4, shipment_date=datetime.datetime.now()),
    Shipment(order_id=5, shipment_date=datetime.datetime.now() + datetime.timedelta(days=3))
]

# Create categories
categories = [
    Category(name='Electronics'),
    Category(name='Accessories'),
    Category(name='Computers')
]

# Create product categories
product_categories = [
    ProductCategory(product_id=1, category_id=1),
    ProductCategory(product_id=1, category_id=3),
    ProductCategory(product_id=2, category_id=1),
    ProductCategory(product_id=3, category_id=1),
    ProductCategory(product_id=4, category_id=2)
]

# Create payments
payments = [
    Payment(order_id=1, amount=1600.0),
    Payment(order_id=2, amount=450.0),
    Payment(order_id=3, amount=700.0),
    Payment(order_id=4, amount=1200.0),
    Payment(order_id=5, amount=240.0)
]

# Create reviews
reviews = [
    Review(product_id=1, customer_id=1, review_text='Great product, fast delivery!', rating=5),
    Review(product_id=2, customer_id=2, review_text='Satisfactory but could be better.', rating=3),
    Review(product_id=3, customer_id=5, review_text='Perfect tablet for my needs!', rating=4),
    Review(product_id=4, customer_id=3, review_text='The headphones are amazing!', rating=5),
    Review(product_id=5, customer_id=4, review_text='Decent monitor for the price.', rating=4)
]

# Add and commit all data
session.add_all(customers + products + orders + order_items + inventory +
                suppliers + supplier_products + shipments + categories +
                product_categories + payments + reviews)

session.commit()
session.close()

print("Database and sample data created successfully.")
