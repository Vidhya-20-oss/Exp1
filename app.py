"""
Flask Web Application for AI Customer Complaint Resolution Agent
Supports:
- Customer Name input
- Order ID input
- Product Defect Image file upload
- Interactive resolution with 4-pillar demonstration
"""

import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from agent import ComplaintResolutionAgent

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max

agent = ComplaintResolutionAgent()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    default_complaint = (
        "I ordered a skincare product five days ago, but I have not received it yet. "
        "The payment was successful."
    )
    result = agent.resolve_complaint(default_complaint)
    return render_template(
        "index.html",
        complaint_input=default_complaint,
        customer_name_input="",
        order_id_input="",
        uploaded_filename=None,
        result=result
    )


@app.route("/resolve", methods=["POST"])
def resolve():
    customer_name = request.form.get("customer_name", "").strip()
    order_id = request.form.get("order_id", "").strip()
    complaint_text = request.form.get("complaint", "").strip()

    uploaded_filename = None
    if "defect_image" in request.files:
        file = request.files["defect_image"]
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            uploaded_filename = filename

    if not complaint_text:
        return render_template(
            "index.html",
            complaint_input="",
            customer_name_input=customer_name,
            order_id_input=order_id,
            uploaded_filename=None,
            result=None
        )

    result = agent.resolve_complaint(
        complaint_text,
        customer_name=customer_name,
        order_id=order_id,
        defect_image=uploaded_filename
    )

    return render_template(
        "index.html",
        complaint_input=complaint_text,
        customer_name_input=customer_name,
        order_id_input=order_id,
        uploaded_filename=uploaded_filename,
        result=result
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    print("Starting AI Customer Complaint Resolution Agent Web UI...")
    print("Open your browser and visit: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
