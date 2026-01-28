import streamlit as st
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🧾 Invoice Generator App",
    page_icon="🧾",
    layout="wide",
)

# ----------------- DARK + GLASSY + NEON CSS -----------------
st.markdown("""
<style>
/* Main dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar glass effect */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Headers */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 600;
}

/* Input fields */
input, textarea, .stNumberInput>div>div>input {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 8px;
}

/* Input focus neon glow */
input:focus, textarea:focus {
    border: 1px solid #00fff7 !important;
    box-shadow: 0 0 8px #00fff7 !important;
    outline: none;
}

/* Buttons */
button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 12px !important;
    padding: 0.5em 1em;
}
button:hover {
    background: linear-gradient(135deg, #764ba2, #667eea) !important;
    box-shadow: 0 0 12px #00fff7 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px;
}

/* Markdown text */
.stMarkdown p {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("🧾 Invoice Generator App")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

if "menu" not in st.session_state:
    st.session_state.menu = "Signup"

menu = st.sidebar.selectbox(
    "Menu",
    ["Signup", "Login", "Dashboard", "Create Invoice"],
    index=["Signup", "Login", "Dashboard", "Create Invoice"].index(st.session_state.menu)
)


# ---------------- SIGNUP ----------------
if menu == "Signup":
    st.subheader("Create Account")

    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Sign Up")

        if submit:
            if not all([full_name, username, email, phone, password, confirm_password]):
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/signup",
                        data={
                            "full_name": full_name,
                            "username": username,
                            "email": email,
                            "phone": phone,
                            "password": password
                        },
                        timeout=5
                    )
                    if res.status_code == 200:
                        st.success("Account created successfully 🎉")
                        st.session_state.menu = "Login"
                        st.rerun()
                    else:
                        st.error(res.json()["detail"])
                except Exception as e:
                    st.error(f"Error: {e}")

# ---------------- LOGIN ----------------
if menu == "Login":
    st.subheader("Login")

    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if not username_or_email or not password:
                st.error("All fields are required")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/login",
                        data={
                            "username_or_email": username_or_email,
                            "password": password
                        },
                        timeout=5
                    )
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.success("Login successful ✅")
                        st.session_state.menu = "Dashboard"
                        st.rerun()
                    else:
                        st.error(res.json()["detail"])
                except Exception as e:
                    st.error(f"Error: {e}")



# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    if not st.session_state.token:
        st.warning("Please login first")
    else:
        st.success("Welcome to Dashboard 🎉")
        st.info("You are logged in securely ✅")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Logout"):
                st.session_state.token = None
                st.session_state.menu = "Login"
                st.rerun()

        with col2:
            if st.button("➕ Create Invoice"):
                st.session_state.menu = "Create Invoice"
                st.rerun()

        st.markdown("---")
        st.subheader("📜 Invoice History")

        if st.session_state.token:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                res = requests.get(f"{API_URL}/invoice-history", headers=headers, timeout=5)
                if res.status_code == 200:
                    invoices = res.json()
                    if invoices:
                        st.table(invoices)
                    else:
                        st.info("No invoices found")
                else:
                    st.error("Failed to fetch invoice history")
            except Exception as e:
                st.error(f"Error: {e}")



# ---------------- CREATE INVOICE ----------------
if menu == "Create Invoice":
    if not st.session_state.token:
        st.warning("Please login first")
    else:
        st.subheader("Create Invoice")

        invoice_data = None  # Store invoice info here

        with st.form("invoice_form"):
            customer_name = st.text_input("Customer Name")
            purchase_order_no = st.text_input("Purchase Order No")
            bill_date = st.date_input("Bill Date")

            billing_address = st.text_area("Billing Address")
            shipping_address = st.text_area("Shipping Address")

            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=1)
            price = st.number_input("Price", min_value=0.0, format="%.2f")

            item_description = st.text_area("Item Description (Optional)")
            additional_details = st.text_area("Additional Details (Optional)")

            submit = st.form_submit_button("Generate Invoice")

            if submit:
                try:
                    headers = {
                        "Authorization": f"Bearer {st.session_state.token}"
                    }
                    
                    res = requests.post(
                        f"{API_URL}/create-invoice",
                        data={
                            "customer_name": customer_name,
                            "purchase_order_no": purchase_order_no,
                            "bill_date": str(bill_date),
                            "billing_address": billing_address,
                            "shipping_address": shipping_address,
                            "item_name": item_name,
                            "quantity": quantity,
                            "price": price,
                            "item_description": item_description,
                            "additional_details": additional_details
                        },
                        headers=headers,   
                        timeout=10
                    )
                    if res.status_code == 200:
                        invoice_data = res.json()  # store response
                        st.success("Invoice Generated ✅")
                        st.write("💰 Total:", invoice_data["total"])
                    else:
                        #st.error("Invoice creation failed")
                        st.error(res.json().get("detail", "Invoice creation failed"))
                except Exception as e:
                    st.error(f"Error: {e}")

        # ---------------- PDF DOWNLOAD BUTTON ----------------
        if invoice_data:
            pdf_path = Path(invoice_data["pdf"])
            if pdf_path.exists():
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Invoice PDF",
                        data=f,
                        file_name=pdf_path.name,
                        mime="application/pdf"
                    )
            else:
                st.error(f"PDF file not found at {pdf_path}")


