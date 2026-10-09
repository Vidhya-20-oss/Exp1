"""
Unit and Integration Tests for AI Customer Complaint Resolution Agent
Validates:
1. Classification, Retrieval, Decision-Making, and Structured Response Generation
2. Customer Name personalization
3. Order ID propagation
4. Product Defect Image verification
"""

import unittest
from agent import ComplaintResolutionAgent


class TestComplaintResolutionAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = ComplaintResolutionAgent()

    def test_criterion_1_classification(self):
        """Verifies issue classification and entity extraction."""
        complaint = "I ordered a skincare product five days ago, but I have not received it yet. The payment was successful."
        res = self.agent.resolve_complaint(complaint)
        c1 = res["demonstrations"]["1_classification"]

        self.assertEqual(c1["category"], "Delivery Issue")
        self.assertEqual(c1["extracted_entities"]["duration"], "five days ago")
        self.assertEqual(c1["extracted_entities"]["payment_status"], "Successful")
        self.assertEqual(c1["extracted_entities"]["product"], "skincare product")

    def test_criterion_2_retrieval(self):
        """Verifies knowledge retrieval of policies, clauses, and SLAs."""
        complaint = "I ordered a skincare product five days ago, but I have not received it yet. The payment was successful."
        res = self.agent.resolve_complaint(complaint)
        c2 = res["demonstrations"]["2_retrieval"]

        self.assertEqual(c2["policy_name"], "Shipping & Logistics Policy")
        self.assertEqual(c2["relevant_clause"], "Check the delivery policy and order-tracking information.")
        self.assertIn("3 to 5 business days", c2["standard_sla"])

    def test_criterion_3_decision_making(self):
        """Verifies decision reasoning, anti-hallucination constraint, and escalation checks."""
        complaint = "I ordered a skincare product five days ago, but I have not received it yet. The payment was successful."
        res = self.agent.resolve_complaint(complaint)
        c3 = res["demonstrations"]["3_decision_making"]

        self.assertTrue(len(c3["reasoning_trace"]) >= 2)
        self.assertIn("No fake order data invented", c3["missing_information_checks"])
        self.assertIn("Escalate to customer support", c3["escalation_condition"])

    def test_criterion_4_structured_response(self):
        """Verifies the exact structured resolution requested in the prompt."""
        complaint = "I ordered a skincare product five days ago, but I have not received it yet. The payment was successful."
        res = self.agent.resolve_complaint(complaint)
        structured = res["structured_output"]

        self.assertEqual(structured["complaint_category"], "Delivery Issue")
        self.assertEqual(
            structured["issue_summary"],
            "The customer has paid for the product but has not received it within five days."
        )
        self.assertEqual(
            structured["retrieved_information"],
            "Check the delivery policy and order-tracking information."
        )
        self.assertEqual(
            structured["recommended_solution"],
            "Verify the order status and provide the expected delivery date. If the order is delayed, initiate the appropriate support process."
        )
        self.assertEqual(
            structured["next_steps"],
            "Ask the customer for the order ID and check the tracking details."
        )
        self.assertEqual(
            structured["escalation"],
            "Escalate to customer support if the shipment is lost or significantly delayed."
        )

    def test_product_defect_with_image_upload(self):
        """Verifies handling when a defect photo is uploaded."""
        complaint = "The moisturizer arrived shattered and leaked."
        res = self.agent.resolve_complaint(
            complaint,
            customer_name="Praveen Kumar",
            order_id="ORD-84912",
            defect_image="broken_cream.jpg"
        )
        structured = res["structured_output"]
        self.assertEqual(structured["complaint_category"], "Product Defect")
        self.assertIn("broken_cream.jpg", structured["recommended_solution"])
        self.assertIn("ORD-84912", structured["next_steps"])
        self.assertIn("Dear Praveen Kumar,", res["customer_response"])

    def test_product_defect_without_image_upload(self):
        """Verifies that missing defect image prompts customer for proof."""
        complaint = "The face wash tube is defective and expired."
        res = self.agent.resolve_complaint(complaint)
        structured = res["structured_output"]
        self.assertEqual(structured["complaint_category"], "Product Defect")
        self.assertIn("request photographs", structured["recommended_solution"].lower())
        self.assertIn("photos of the damaged item", structured["next_steps"].lower())

    def test_payment_category(self):
        """Tests classification and retrieval for payment discrepancies."""
        complaint = "My credit card was debited twice for order #88432, but no confirmation was generated."
        res = self.agent.resolve_complaint(complaint)
        self.assertEqual(res["structured_output"]["complaint_category"], "Payment Issue")

    def test_refund_category(self):
        """Tests classification and retrieval for refund requests."""
        complaint = "I cancelled order #1042 five days ago and still have not received my refund."
        res = self.agent.resolve_complaint(complaint)
        self.assertEqual(res["structured_output"]["complaint_category"], "Refund")

    def test_service_category(self):
        """Tests classification and retrieval for service dissatisfaction."""
        complaint = "The chat representative was extremely rude and unhelpful."
        res = self.agent.resolve_complaint(complaint)
        self.assertEqual(res["structured_output"]["complaint_category"], "Service Issue")


if __name__ == "__main__":
    unittest.main()
