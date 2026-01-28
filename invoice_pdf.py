from fpdf import FPDF
from pathlib import Path

def generate_invoice_pdf(invoice):
    # Create 'invoices' folder inside backend if it doesn't exist
    invoices_dir = Path(__file__).parent / "invoices"
    invoices_dir.mkdir(exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Customer: {invoice.customer_name}", ln=True)
    pdf.cell(0, 8, f"PO No: {invoice.purchase_order_no}", ln=True)
    pdf.cell(0, 8, f"Bill Date: {invoice.bill_date}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, f"Billing Address: {invoice.billing_address}", ln=True)
    pdf.cell(0, 8, f"Shipping Address: {invoice.shipping_address}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, f"Item: {invoice.item_name}", ln=True)
    pdf.cell(0, 8, f"Qty: {invoice.quantity}", ln=True)
    pdf.cell(0, 8, f"Price: {invoice.price}", ln=True)
    pdf.cell(0, 8, f"Total: {invoice.total}", ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Description: {invoice.item_description}")
    pdf.multi_cell(0, 8, f"Additional Details: {invoice.additional_details}")

    # Save PDF in invoices folder
    pdf_filename = f"invoice_{invoice.id}.pdf"
    pdf_path = invoices_dir / pdf_filename
    pdf.output(str(pdf_path))

    # Return full path
    return str(pdf_path)
