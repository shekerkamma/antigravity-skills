from typing import Dict, Any

class PreflightSimulator:
    """
    PreflightSimulator runs simulation loops (Trend 8) to catch validation errors
    and prevent automated database corruption or unauthorized transactions
    before committing database changes.
    """
    def __init__(self):
        # Policy rules
        self.max_refund_limit = 1000.0
        self.allowed_license_resets_per_month = 3

    def simulate_refund(self, email: str, amount: float, days_since_purchase: int) -> Dict[str, Any]:
        """
        Simulates refund processing and returns eligibility results.
        """
        checks = {
            "under_limit": amount <= self.max_refund_limit,
            "within_return_window": days_since_purchase <= 30,
            "account_active": True # Assume active for mock
        }

        eligible = all(checks.values())
        
        reasons = []
        if not checks["under_limit"]:
            reasons.append(f"Refund amount ${amount} exceeds the $1000 limit.")
        if not checks["within_return_window"]:
            reasons.append(f"Purchase date ({days_since_purchase} days ago) is outside the 30-day window.")

        return {
            "action": "refund",
            "eligible": eligible,
            "reasons": reasons,
            "simulation_checks": checks,
            "status": "APPROVED" if eligible else "REJECTED"
        }

    def simulate_license_reset(self, email: str, active_resets: int) -> Dict[str, Any]:
        """
        Simulates license key reset and returns feasibility results.
        """
        checks = {
            "under_reset_limit": active_resets < self.allowed_license_resets_per_month,
            "domain_authorized": not email.endswith(".temp") # block temp domains
        }

        eligible = all(checks.values())

        reasons = []
        if not checks["under_reset_limit"]:
            reasons.append("Maximum monthly license resets exceeded.")
        if not checks["domain_authorized"]:
            reasons.append("Unauthorized email domain.")

        return {
            "action": "license_reset",
            "eligible": eligible,
            "reasons": reasons,
            "simulation_checks": checks,
            "status": "APPROVED" if eligible else "REJECTED"
        }
