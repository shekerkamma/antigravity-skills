# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.events.event import Event
from google.adk.agents.context import Context
from google.genai import Client, types
from app.prompts.system_prompts import SHIPPING_FAQ_INSTRUCTION
from app.services.datastore import get_shipping_faq_kb
from app.security.output_guards import scrub_pii_and_placeholders

# Resolve knowledge base static content into system prompt instructions
kb_data = get_shipping_faq_kb()
formatted_instruction = SHIPPING_FAQ_INSTRUCTION.format(knowledge_base=kb_data)

def shipping_faq_agent(ctx: Context, node_input: str) -> Event:
    """Executes the FAQ query via Gemini client and validates output security before rendering."""
    # Initialize the standard Google GenAI client
    client = Client()
    
    # Execute generation directly
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=node_input,
        config=types.GenerateContentConfig(
            system_instruction=formatted_instruction
        )
    )
    
    # Process text output through security guards (Layer 4)
    raw_text = response.text or ""
    safe_output = scrub_pii_and_placeholders(raw_text)
    
    # Return single consolidated Event
    return Event(
        content=types.Content(
            role="model", parts=[types.Part.from_text(text=safe_output)]
        ),
        output=safe_output,
    )
