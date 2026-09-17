from typing import Dict, Any, Optional

class EnrichmentOrchestrator:
    """
    EnrichmentOrchestrator implements the 'Clay Paradigm' for customer support.
    It orchestrates data aggregation from ServiceNow, Jira Service Management (JSM),
    Hubspot (CRM), and Stripe (Billing) to clean and validate incoming ticket data.
    """
    def __init__(self):
        # Simulated database for demo purposes
        self.stripe_db = {
            "customer@enterprise.com": {
                "customer_id": "cus_N8x9102",
                "tier": "Enterprise Premium",
                "status": "active",
                "mrr": 4500.0,
                "delinquent": False
            },
            "user@startup.io": {
                "customer_id": "cus_S2a8190",
                "tier": "Growth Flat-rate",
                "status": "active",
                "mrr": 499.0,
                "delinquent": False
            }
        }
        
        self.hubspot_db = {
            "customer@enterprise.com": {
                "account_owner": "Sarah Jenkins (Enterprise Sales Director)",
                "churn_risk": "low",
                "recent_sales_note": "Expanding account. Planning to purchase 50 additional licenses in Q3. Keep happy.",
                "support_tier": "VIP-Platinum"
            },
            "user@startup.io": {
                "account_owner": "Automated SMB Queue",
                "churn_risk": "high",
                "recent_sales_note": "Concerned about token API pricing overhead. Needs optimization suggestions.",
                "support_tier": "Standard"
            }
        }

        self.servicenow_db = {
            "INC-10928": {
                "sys_id": "sn_inc_829102",
                "impact": "High",
                "urgency": "Medium",
                "category": "Software",
                "assignment_group": "Tier 3 Operations"
            }
        }

        self.jira_db = {
            "SUPPORT-504": {
                "ticket_id": "jira_t_89201",
                "priority": "High",
                "component": "License Manager",
                "status": "In Progress"
            }
        }

    def fetch_all(self, email: str, ticket_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gathers data from multiple systems based on email and ticket_id.
        """
        stripe_info = self.stripe_db.get(email, {
            "customer_id": "N/A",
            "tier": "Free / Trial",
            "status": "inactive",
            "mrr": 0.0,
            "delinquent": False
        })
        
        hubspot_info = self.hubspot_db.get(email, {
            "account_owner": "Unassigned",
            "churn_risk": "unknown",
            "recent_sales_note": "No notes found.",
            "support_tier": "Standard"
        })

        servicenow_info = {}
        if ticket_id and ticket_id.startswith("INC"):
            servicenow_info = self.servicenow_db.get(ticket_id, {
                "sys_id": "unknown",
                "impact": "Low",
                "urgency": "Low",
                "category": "General Inquiry",
                "assignment_group": "Tier 1 Helpdesk"
            })

        jira_info = {}
        if ticket_id and ticket_id.startswith("SUPPORT"):
            jira_info = self.jira_db.get(ticket_id, {
                "ticket_id": "unknown",
                "priority": "Medium",
                "component": "General",
                "status": "Open"
            })

        return {
            "customer_email": email,
            "ticket_id": ticket_id,
            "stripe": stripe_info,
            "crm": hubspot_info,
            "servicenow": servicenow_info,
            "jira": jira_info
        }
