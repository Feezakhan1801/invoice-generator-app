from sqlalchemy import Column, Integer, String,Float, Date, ForeignKey
from backend.database import Base


class User(Base):
    __tablename__ = "users_invoice"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Invoice(Base):
    __tablename__ = "invoice_table"

    id = Column(Integer, primary_key=True, index=True)
    
    
    customer_name = Column(String, nullable=False)
    purchase_order_no = Column(String, nullable=False)
    bill_date = Column(String, nullable=False)

    billing_address = Column(String, nullable=False)
    shipping_address = Column(String, nullable=False)

    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    item_description = Column(String)
    additional_details = Column(String)
    
    user_id = Column(Integer, ForeignKey("users_invoice.id"))  # ✅ logged-in user
