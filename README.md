# Experiment 1: AI Customer Complaint Resolution Agent

## Aim
To design, implement, and demonstrate an AI Customer Complaint Resolution Agent that receives customer complaints, classifies the issue, retrieves relevant product/service policies, evaluates defect proof and order identifiers, determines appropriate resolution strategies through constrained decision-making, and generates standardized structured responses.

---

## The 4 Demonstrated Core Competencies

### 1. Classification & Entity Extraction
* **Categorization**: Classifies incoming complaints into 5 canonical categories:
  - `Delivery Issue`
  - `Payment Issue`
  - `Product Defect`
  - `Refund`
  - `Service Issue`
* **Entity & Metadata Extraction**:
  - **Customer Name**: Used for personalized customer-facing communication.
  - **Order ID**: Dedicated input field or extracted regex match (e.g., `ORD-84912`).
  - **Product Defect Proof**: Attached image verification indicator.
  - **Time Elapsed**: Extracted duration (e.g., *"five days ago"*).
  - **Payment Status**: Successful / failed / unverified.

### 2. Information Retrieval
* Queries the domain knowledge base ([policies.json](policies.json)) to retrieve:
  - Official Policy Document (e.g., *Product Quality & Replacement Policy*, *Shipping & Logistics Policy*)
  - Applicable Policy Clause
  - Standard Service Level Agreement (SLA) timelines (e.g., *7-day replacement window*, *3 to 5 business days*)
  - Relevant FAQs

### 3. Decision-Making & Anti-Hallucination Guardrails
* **Defect Photographic Proof Verification**: If a product defect image is uploaded, damage verification is satisfied and immediate replacement is approved. If not uploaded, the agent requests photo proof.
* **Order ID Validation**: If an Order ID is present, the agent targets that specific order in courier tracking. If missing, the agent requests it without fabricating details.
* **Escalation Protocol**: Flags cases requiring supervisor intervention (e.g., lost transit, health safety reactions).

### 4. Structured Response Generation
* Emits a standardized 6-field structured resolution block:
  1. `Complaint Category`
  2. `Issue Summary`
  3. `Retrieved Information`
  4. `Recommended Solution`
  5. `Next Steps`
  6. `Escalation`
* Produces an empathetic, personalized customer-facing response.

---

## Project Structure

```
d:\Exp1\
│
├── agent.py            # Core Agent Engine (Classification, Retrieval, Decision, Generation)
├── policies.json       # Knowledge base (Policies, SLAs, FAQs)
├── cli.py              # Interactive console interface supporting Name, Order ID, and Defect upload
├── app.py              # Flask Web application supporting file upload & multipart forms
├── test_agent.py       # Unit test suite verifying all 4 criteria and field combinations
├── uploads/            # Storage directory for uploaded product defect images
├── templates/
│   └── index.html      # Responsive Web UI with Name, Order ID, Defect Image upload, and previews
└── README.md           # Experiment documentation
```

---

## How to Run

### 1. Verification Script (Terminal)
```powershell
python d:\Exp1\agent.py
```

### 2. Interactive CLI Tool
```powershell
python d:\Exp1\cli.py
```

### 3. Automated Test Suite (9 Tests Passing)
```powershell
python d:\Exp1\test_agent.py
```

### 4. Web Application (With File Upload & Field Inputs)
```powershell
python d:\Exp1\app.py
```
Open browser at: `http://127.0.0.1:5000`
