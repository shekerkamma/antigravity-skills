from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.quiet_context.service import QuietContextService

router = APIRouter(prefix="/api/v1", tags=["QuietContext"])
service = QuietContextService()

class TicketRequest(BaseModel):
    ticket_id: str
    customer_email: str
    raw_query: str

class TicketResponse(BaseModel):
    summary: str
    data_enrichment: Dict[str, Any]
    simulated_actions: Dict[str, Any]
    audit_trail: Dict[str, Any]

@router.post("/enrich-ticket", response_model=TicketResponse)
async def enrich_ticket(request: TicketRequest):
    """
    QuietContext AI Ticket Enrichment Endpoint.
    Designed for silent integration (Trend 4) with ServiceNow and Jira (Trend 10).
    Redacts PII (Trend 9), optimizes tokens via semantic caching (Trend 6),
    enriches context from CRM/Stripe (Trend 3), and executes pre-flight checks (Trend 8).
    """
    try:
        result = service.process_ticket(
            raw_query=request.raw_query,
            customer_email=request.customer_email,
            ticket_id=request.ticket_id
        )
        return TicketResponse(
            summary=result["summary"],
            data_enrichment=result["data_enrichment"],
            simulated_actions=result["simulated_actions"],
            audit_trail=result["audit_trail"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
