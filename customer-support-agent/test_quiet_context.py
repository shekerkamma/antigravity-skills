import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.quiet_context.service import QuietContextService

def run_tests():
    print("Initializing QuietContextService...")
    service = QuietContextService()

    # Define test tickets
    tickets = [
        {
            "ticket_id": "INC-10928",
            "customer_email": "customer@enterprise.com",
            "raw_query": "Hello, my name is Alice Vance (SSN: 123-45-6789). I would like to request a refund for order #10029, because our team is looking to downscale our enterprise plan. Can we get our money back?"
        },
        {
            "ticket_id": "SUPPORT-504",
            "customer_email": "user@startup.io",
            "raw_query": "Hi support, my credit card is 4111-2222-3333-4444. I need to reset my license key since we are migrating our servers. Can you assist with the reset?"
        },
        {
            "ticket_id": "SUPPORT-505", # Cache hit test
            "customer_email": "customer@enterprise.com",
            "raw_query": "Hello, my name is John Doe (SSN: 987-65-4321). I would like to request a refund for order #10029, because our team is looking to downscale our enterprise plan. Can we get our money back?"
        }
    ]

    for idx, ticket in enumerate(tickets, start=1):
        print(f"\n================ TEST CASE {idx} ================")
        result = service.process_ticket(
            raw_query=ticket["raw_query"],
            customer_email=ticket["customer_email"],
            ticket_id=ticket["ticket_id"]
        )
        print("\n[RESULT SUMMARY]")
        print(result["summary"])
        print("\n[DATA ENRICHMENT]")
        print(result["data_enrichment"])
        print("\n[SIMULATED ACTIONS]")
        print(result["simulated_actions"])
        print("\n[AUDIT TRAIL]")
        print(result["audit_trail"])

if __name__ == "__main__":
    run_tests()
