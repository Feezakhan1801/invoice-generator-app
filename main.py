from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine,Base
from backend.models import User, Invoice
from backend.auth import hash_password, verify_password, create_access_token,get_current_user
from backend.invoice_pdf import generate_invoice_pdf
import re

app = FastAPI()

# ---------- CREATE TABLES ----------
User.metadata.create_all(bind=engine)
Invoice.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

# ---------- DB DEPENDENCY ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- VALIDATIONS ----------
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return (
        len(password) >= 8
        and re.search("[A-Z]", password)
        and re.search("[0-9]", password)
    )

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

# ---------- SIGNUP ----------
@app.post("/signup")
def signup(
    full_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if not validate_phone(phone):
        raise HTTPException(status_code=400, detail="Phone must be 10 digits")

    if not validate_password(password):
        raise HTTPException(
            status_code=400,
            detail="Password must have 8 chars, 1 capital letter & 1 number"
        )

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        phone=phone,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {"message": "Signup successful"}

# ---------- LOGIN ----------
@app.post("/login")
def login(
    username_or_email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if re.match(r"[^@]+@[^@]+\.[^@]+", username_or_email):
        user = db.query(User).filter(User.email == username_or_email).first()
    else:
        user = db.query(User).filter(User.username == username_or_email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"sub": user.username})

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email
        }
    }

# ---------- CREATE INVOICE ----------
@app.post("/create-invoice")
def create_invoice(
    customer_name: str = Form(...),
    purchase_order_no: str = Form(...),
    bill_date: str = Form(...),
    billing_address: str = Form(...),
    shipping_address: str = Form(...),
    item_name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    item_description: str = Form(""),
    additional_details: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ logged-in user
    
):
    total = quantity * price

    invoice = Invoice(
        customer_name=customer_name,
        purchase_order_no=purchase_order_no,
        bill_date=bill_date,
        billing_address=billing_address,
        shipping_address=shipping_address,
        item_name=item_name,
        quantity=quantity,
        price=price,
        total=total,
        item_description=item_description,
        additional_details=additional_details,
        user_id=current_user.id  # ✅ save user_id
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    pdf_path = generate_invoice_pdf(invoice)

    return {
        "message": "Invoice created successfully",
        "invoice_id": invoice.id,
        "total": total,
        "pdf": pdf_path
    }


# ---------- GET INVOICE HISTORY FOR LOGGED-IN USER ----------
@app.get("/invoice-history")
def invoice_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ logged-in user
):
    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).order_by(Invoice.id.desc()).all()
    return [
        {
            "ID": i.id,
            "Customer": i.customer_name,
            "PO No": i.purchase_order_no,
            "Date": i.bill_date,
            "Quantity":i.quantity,
            "Price":i.price,
            "Total": i.total
        }
        for i in invoices
    ]