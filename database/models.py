# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 15, 2024 15:46:55
# Database: sqlite:////tmp/tmp.bB2L7e9OK9/lb/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Category(SAFRSBaseX, Base):
    """
    description: Categories to categorize different products.
    """
    __tablename__ = 'categories'
    _s_collection_name = 'Category'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="category")



class Customer(SAFRSBaseX, Base):
    """
    description: Customers with personal data, balance, and credit limit.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    credit_limit = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="customer")



class Product(SAFRSBaseX, Base):
    """
    description: Products available for purchase with detailed information.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="product")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="product")
    SupplierProductList : Mapped[List["SupplierProduct"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")



class Supplier(SAFRSBaseX, Base):
    """
    description: Suppliers providing products to be sold.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    SupplierProductList : Mapped[List["SupplierProduct"]] = relationship(back_populates="supplier")



class Inventory(SAFRSBaseX, Base):
    """
    description: Inventory details for products including stock levels.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    stock = Column(Integer, nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Orders made by customers, including a notes field.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, nullable=False)
    notes = Column(String)
    amount_total = Column(Float, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="order")



class ProductCategory(SAFRSBaseX, Base):
    """
    description: Many-to-many relationship between products and categories.
    """
    __tablename__ = 'product_categories'
    _s_collection_name = 'ProductCategory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

    # parent relationships (access parent)
    category : Mapped["Category"] = relationship(back_populates=("ProductCategoryList"))
    product : Mapped["Product"] = relationship(back_populates=("ProductCategoryList"))

    # child relationships (access children)



class Review(SAFRSBaseX, Base):
    """
    description: Customer reviews of products.
    """
    __tablename__ = 'reviews'
    _s_collection_name = 'Review'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    review_text = Column(String)
    rating = Column(Integer, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReviewList"))
    product : Mapped["Product"] = relationship(back_populates=("ReviewList"))

    # child relationships (access children)



class SupplierProduct(SAFRSBaseX, Base):
    """
    description: Relationship between suppliers and products they provide.
    """
    __tablename__ = 'supplier_products'
    _s_collection_name = 'SupplierProduct'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("SupplierProductList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("SupplierProductList"))

    # child relationships (access children)



class OrderItem(SAFRSBaseX, Base):
    """
    description: Items within an order, linking products and orders together.
    """
    __tablename__ = 'order_items'
    _s_collection_name = 'OrderItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Payment information linked to orders.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Shipment(SAFRSBaseX, Base):
    """
    description: Shipments related to orders for delivery purposes.
    """
    __tablename__ = 'shipments'
    _s_collection_name = 'Shipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    shipment_date = Column(DateTime)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShipmentList"))

    # child relationships (access children)
