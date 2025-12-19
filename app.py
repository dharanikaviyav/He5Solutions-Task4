from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from db import get_db
import io

app = Flask(__name__)
CORS(app)

@app.route("/api/invoice", methods=["POST"])
def save_invoice():
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO invoices (client_name) VALUES (%s)",
        (data["client_name"],)
    )
    invoice_id = cur.lastrowid

    for item in data["items"]:
        cur.execute(
            "INSERT INTO invoice_items (invoice_id,item,qty,price) VALUES (%s,%s,%s,%s)",
            (invoice_id, item["name"], item["qty"], item["price"])
        )

    db.commit()
    return jsonify({"status": "saved"})

@app.route("/api/invoice/pdf")
def generate_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "INVOICE")

    y = 760
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM invoices ORDER BY id DESC LIMIT 1")
    invoice = cur.fetchone()

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Client: {invoice['client_name']}")
    y -= 30

    cur.execute("SELECT * FROM invoice_items WHERE invoice_id=%s", (invoice["id"],))
    items = cur.fetchall()

    for item in items:
        pdf.drawString(50, y, f"{item['item']}  x{item['qty']}  ₹{item['price']}")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="invoice.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
