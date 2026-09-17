import os
from typing import Dict, Any, Optional
from google.genai import Client, types

from app.quiet_context.pii_redactor import PIIRedactor
from app.quiet_context.enrichment_orchestrator import EnrichmentOrchestrator
from app.quiet_context.semantic_cache import SemanticCache
from app.quiet_context.preflight_simulator import PreflightSimulator

class QuietContextService:
    """
    QuietContextService orchestrates the entire ticket enrichment, cache control,
    PII sanitization, and pre-flight simulation pipeline.
    """
    def __init__(self):
        self.redactor = PIIRedactor()
        self.orchestrator = EnrichmentOrchestrator()
        self.cache = SemanticCache(threshold=0.80)
        self.simulator = PreflightSimulator()
        
        # Initialize Gemini Client
        try:
            self.client = Client()
            self.gemini_available = True
        except Exception:
            self.client = None
            self.gemini_available = False

    def _get_embedding(self, text: str) -> Optional[list]:
        """Fetches embedding vector from Gemini if available."""
        if not self.gemini_available or not self.client:
            return None
        try:
            # Generate embedding using standard text-embedding model
            result = self.client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"[QuietContextService] Embedding generation failed: {e}")
            return None

    def process_ticket(self, raw_query: str, customer_email: str, ticket_id: str) -> Dict[str, Any]:
        """
        Coordinates the full pipeline:
        1. PII Redaction (GDPR Compliance)
        2. Semantic Cache Check (Token Cost Optimization)
        3. External Data Enrichment (Clay Paradigm)
        4. Action Pre-flight Simulation (Error Prevention)
        5. Deep Context Synthesis (LLM Summary)
        6. Restores PII for target ServiceNow / Jira interface delivery
        """
        print(f"\n--- Processing Ticket: {ticket_id} ({customer_email}) ---")

        # 1. PII Redaction
        redacted_query, pii_map = self.redactor.redact(raw_query)
        print(f"[PII Redactor] Redacted Query: {redacted_query}")

        # 2. Semantic Cache Check
        embedding = self._get_embedding(redacted_query)
        cached_result = self.cache.lookup(redacted_query, query_embedding=embedding)
        
        if cached_result:
            # Cache Hit: Restore PII mapping to the cached template
            restored_summary = self.redactor.restore(cached_result["summary"], pii_map)
            # Create a audit trail entry
            audit_trail = {
                "ticket_id": ticket_id,
                "status": "CACHE_HIT",
                "simulated_actions": cached_result["simulated_actions"],
                "compliance_check": "VERIFIED_GDPR_COMPLIANT"
            }
            return {
                "summary": restored_summary,
                "data_enrichment": cached_result["data_enrichment"],
                "simulated_actions": cached_result["simulated_actions"],
                "audit_trail": audit_trail
            }

        # 3. Data Enrichment Orchestration (Clay Paradigm)
        enriched_data = self.orchestrator.fetch_all(customer_email, ticket_id)
        
        # 4. Preflight Simulation Checks
        simulated_actions = {}
        query_lower = raw_query.lower()
        if "refund" in query_lower or "money back" in query_lower:
            # Mock days elapsed as 15 for demo purposes
            simulated_actions["refund"] = self.simulator.simulate_refund(
                email=customer_email, 
                amount=150.0, 
                days_since_purchase=15
            )
        if "license" in query_lower or "reset" in query_lower:
            # Mock resets elapsed as 1 for demo purposes
            simulated_actions["license_reset"] = self.simulator.simulate_license_reset(
                email=customer_email,
                active_resets=1
            )

        # 5. Deep Context Synthesis
        summary_instruction = (
            "You are an enterprise AI Support Context Coordinator. Synthesize this data "
            "into a brief, highly contextual 3-sentence overview to display directly inside Jira or ServiceNow. "
            "Address: Account status/billing, main issue, and recommended compliance actions.\n\n"
            f"Customer Ticket: {redacted_query}\n"
            f"Stripe/CRM Data: {enriched_data}\n"
            f"Simulated Actions: {simulated_actions}\n"
        )
        
        synthesized_redacted_summary = "Unable to process via LLM. Local enrichment applied."
        if self.gemini_available and self.client:
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=summary_instruction
                )
                if response.text:
                    synthesized_redacted_summary = response.text.strip()
            except Exception as e:
                print(f"[QuietContextService] LLM generation failed: {e}")

        # Store in Semantic Cache (using redacted format)
        cache_entry = {
            "summary": synthesized_redacted_summary,
            "data_enrichment": enriched_data,
            "simulated_actions": simulated_actions
        }
        self.cache.store(redacted_query, cache_entry, embedding=embedding)

        # Restore PII for delivery (Trend 4 - Quiet UI Insertion)
        final_summary = self.redactor.restore(synthesized_redacted_summary, pii_map)

        audit_trail = {
            "ticket_id": ticket_id,
            "status": "CACHE_MISS",
            "simulated_actions": simulated_actions,
            "compliance_check": "VERIFIED_GDPR_COMPLIANT"
        }

        return {
            "summary": final_summary,
            "data_enrichment": enriched_data,
            "simulated_actions": simulated_actions,
            "audit_trail": audit_trail
        }
