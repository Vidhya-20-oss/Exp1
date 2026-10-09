"""
Interactive Command-Line Interface for AI Customer Complaint Resolution Agent
Demonstrates: Classification, Retrieval, Decision-Making, and Structured Response Generation.
Supports: Customer Name, Order ID, and Product Defect Image Proof.
"""

import sys
from agent import ComplaintResolutionAgent

def print_separator(char="=", length=70):
    print(char * length)

def display_result(agent: ComplaintResolutionAgent, result: dict):
    demos = result["demonstrations"]
    structured = result["structured_output"]

    print_separator("-")
    print("DEMONSTRATION 1: CLASSIFICATION")
    print(f"  * Detected Category : {demos['1_classification']['category']}")
    print(f"  * Indicator Reasons : {', '.join(demos['1_classification']['indicators'])}")
    print(f"  * Extracted Entities: {demos['1_classification']['extracted_entities']}")

    print("\nDEMONSTRATION 2: INFORMATION RETRIEVAL")
    print(f"  * Knowledge Source  : {demos['2_retrieval']['policy_name']}")
    print(f"  * Retrieved Clause  : {demos['2_retrieval']['relevant_clause']}")
    print(f"  * Operating SLA     : {demos['2_retrieval']['standard_sla']}")

    print("\nDEMONSTRATION 3: DECISION-MAKING & REASONING")
    for step in demos['3_decision_making']['reasoning_trace']:
        print(f"  * Reasoning Step    : {step}")
    print(f"  * Escalation Path   : {demos['3_decision_making']['escalation_condition']}")

    print("\nDEMONSTRATION 4: STRUCTURED RESPONSE GENERATION")
    print(f"Complaint Category   : {structured['complaint_category']}")
    print(f"Issue Summary        : {structured['issue_summary']}")
    print(f"Retrieved Information: {structured['retrieved_information']}")
    print(f"Recommended Solution : {structured['recommended_solution']}")
    print(f"Next Steps           : {structured['next_steps']}")
    print(f"Escalation           : {structured['escalation']}")

    print_separator("-")
    print("CUSTOMER-FACING RESPONSE:")
    print_separator("-")
    print(result["customer_response"])
    print_separator("=")

def main():
    agent = ComplaintResolutionAgent()
    print_separator("=")
    print("   AI CUSTOMER COMPLAINT RESOLUTION SYSTEM")
    print("   Demonstrating: Classification | Retrieval | Decision | Generation")
    print_separator("=")

    sample_complaints = [
        {
            "label": "Delivery Issue (Lab Prompt)",
            "name": "",
            "order_id": "",
            "defect_image": "",
            "complaint": "I ordered a skincare product five days ago, but I have not received it yet. The payment was successful."
        },
        {
            "label": "Product Defect (With Proof & Order ID)",
            "name": "Praveen Kumar",
            "order_id": "ORD-84912",
            "defect_image": "broken_cream_seal.jpg",
            "complaint": "The moisturizing cream bottle was broken upon delivery and the lotion leaked inside the box."
        },
        {
            "label": "Payment Double-Charge",
            "name": "Dharshini",
            "order_id": "ORD-99321",
            "defect_image": "",
            "complaint": "My credit card was debited twice for order ORD-99321, but no invoice was generated."
        },
        {
            "label": "Refund Request",
            "name": "Rahul",
            "order_id": "ORD-1042",
            "defect_image": "",
            "complaint": "I cancelled order ORD-1042 five days ago and still have not received my refund."
        },
        {
            "label": "Service Issue",
            "name": "Ananya",
            "order_id": "",
            "defect_image": "",
            "complaint": "The chat representative was extremely rude and ended the session without assisting me."
        }
    ]

    while True:
        print("\nSelect an option:")
        print("1. Run Sample Complaint from Lab Prompt")
        print("2. Enter a Custom Customer Complaint (With Name, Order ID & Defect Photo)")
        print("3. Run Pre-configured Test Cases (All Categories)")
        print("4. Exit")
        
        choice = input("\nEnter choice [1-4]: ").strip()

        if choice == "1":
            item = sample_complaints[0]
            print_separator()
            print(f"Input: \"{item['complaint']}\"")
            res = agent.resolve_complaint(item['complaint'])
            display_result(agent, res)

        elif choice == "2":
            name = input("\nEnter Customer Name (optional, press Enter to skip): ").strip()
            oid = input("Enter Order ID (optional, press Enter to skip): ").strip()
            defect_img = input("Enter Product Defect image filename (optional, e.g. broken_item.jpg): ").strip()
            complaint = input("Enter Customer Complaint details (required):\n> ").strip()

            if not complaint:
                print("Error: Complaint text cannot be empty.")
                continue

            res = agent.resolve_complaint(
                complaint_text=complaint,
                customer_name=name if name else None,
                order_id=oid if oid else None,
                defect_image=defect_img if defect_img else None
            )
            display_result(agent, res)

        elif choice == "3":
            for idx, item in enumerate(sample_complaints, 1):
                print(f"\n[Test Case {idx}: {item['label']}]")
                if item['name']:
                    print(f"Customer Name: {item['name']} | Order ID: {item['order_id']} | Defect Proof: {item['defect_image'] or 'None'}")
                print(f"Input: \"{item['complaint']}\"")
                res = agent.resolve_complaint(
                    complaint_text=item['complaint'],
                    customer_name=item['name'] if item['name'] else None,
                    order_id=item['order_id'] if item['order_id'] else None,
                    defect_image=item['defect_image'] if item['defect_image'] else None
                )
                display_result(agent, res)

        elif choice == "4":
            print("\nExiting. Thank you!")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
