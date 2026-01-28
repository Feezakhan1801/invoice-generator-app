# invoice-generator-app

🧾 Invoice Generator App

A full-stack Invoice Generator Application built using FastAPI (Backend) and Streamlit (Frontend) with JWT Authentication, PDF Invoice generation, and User-specific Invoice History.

🚀 Features

🔐 User Authentication

Signup & Login

Password hashing using bcrypt

JWT-based secure authentication

🧾 Invoice Management

Create invoices with customer & product details

Auto calculate total amount

Generate PDF invoices

Download invoices instantly

📜 Invoice History

Logged-in users can view only their own invoices

Secure user-invoice mapping

🎨 Modern UI

Streamlit frontend

Dark, glassy, neon-style interface

🛠️ Tech Stack
Backend

FastAPI

SQLAlchemy

SQLite

JWT (python-jose)

Passlib + Bcrypt

FPDF (PDF generation)

Frontend

Streamlit

Requests

📁 Project Structure
invoice_app/
│
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── invoice_pdf.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Feezakhan1801/invoice-generator-app.git
cd invoice-generator-app

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Running the Application
🔹 Start Backend (FastAPI)
uvicorn backend.main:app --reload


Backend will run at:

http://127.0.0.1:8000

🔹 Start Frontend (Streamlit)

Open new terminal:

streamlit run frontend/app.py


Frontend will run at:

http://localhost:8501

🔑 API Endpoints
Method	Endpoint	Description
POST	/signup	Create new user
POST	/login	Login user
POST	/create-invoice	Create invoice (JWT required)
GET	/invoice-history	Get user invoice history
🔐 Authentication Flow

User signs up

User logs in

Backend returns JWT access token

Frontend stores token in session

Token is sent in headers:

Authorization: Bearer <token>


Only authenticated users can create/view invoices

📄 Invoice PDF Generation

PDFs are generated using FPDF

Stored inside:

backend/invoices/


Downloadable directly from frontend

⚠️ Security Notes

Change SECRET_KEY in auth.py before production

Do not commit:

venv/

.db files

Generated PDFs

🌱 Future Improvements

Email invoice feature

Admin dashboard

Cloud database (PostgreSQL)

Deployment (Render / Railway / AWS)

Role-based access

👩‍💻 Author

Feeza Khan
GitHub: Feezakhan1801

⭐ Support

If you like this project, don’t forget to ⭐ star the repository!
