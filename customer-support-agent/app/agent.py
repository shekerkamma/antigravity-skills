# ruff: noqa
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

import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# If using GOOGLE_API_KEY / GEMINI_API_KEY, use non-vertex setup
if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    try:
        import google.auth

        _, project_id = google.auth.default()
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    except Exception:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

from google.adk.workflow import Workflow
from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions
from google.adk.agents.context import Context
from google.genai import types
from pydantic import BaseModel, Field


# 1. Pydantic Model for routing
class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user query is about shipping (rates, tracking, delivery, returns). False otherwise."
    )


# 2. Classifier Agent
classifier_agent = LlmAgent(
    name="classifier_agent",
    model="gemini-2.5-flash",
    instruction=(
        "Analyze the user's input. Classify if the query is related to shipping (such as rates, "
        "tracking, delivery, or returns) or unrelated. Output your decision according to the schema."
    ),
    output_schema=Classification,
    output_key="classification",
)


# 3. Router function node to inspect classification and route
def route_query(ctx: Context, node_input: dict) -> Event:
    # Extract the original user text query
    user_text = ""
    if ctx.user_content and ctx.user_content.parts:
        user_text = "".join(part.text for part in ctx.user_content.parts if part.text)

    is_shipping = node_input.get("is_shipping_related", False)
    if is_shipping:
        return Event(output=user_text, actions=EventActions(route="shipping"))
    else:
        return Event(output=user_text, actions=EventActions(route="unrelated"))


# 4. Shipping FAQ Agent
shipping_faq_agent = LlmAgent(
    name="shipping_faq_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are an enthusiastic and friendly customer support representative for a shipping company! 🚚✨\n"
        "Use the following knowledge base to answer the user's shipping query:\n"
        "- **Standard Shipping**: Costs $5.99. **🚨 FREE SHIPPING FOR ORDERS OVER $50! 🎉** Delivery takes 3-5 business days. 📦\n"
        "- **Expedited Shipping**: Costs $15.00. Delivery takes 1-2 business days. ⚡\n"
        "- **Tracking**: Customers can track orders using their tracking ID on our website. 🔍\n"
        "- **Returns**: Returns are accepted within 30 days of delivery. Return shipping is free! 🔄\n\n"
        "Be extremely playful, cheerful, and enthusiastic in your responses! When responding to queries about shipping rates, "
        "make sure to enthusiastically highlight the **FREE shipping threshold** for orders over $50, and use plenty of emojis!"
    ),
)


# 5. Decline Node (polite decline)
def decline_to_answer(ctx: Context) -> Event:
    decline_text = (
        "I apologize, but I can only assist with shipping-related queries like rates, "
        "tracking, delivery, and returns. How can I help you with your shipment today?"
    )
    # Output the message to the user UI using content, and also output value
    return Event(
        content=types.Content(
            role="model", parts=[types.Part.from_text(text=decline_text)]
        ),
        output=decline_text,
    )


# 6. Workflow Agent
root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        ("START", classifier_agent),
        (classifier_agent, route_query),
        (route_query, {"shipping": shipping_faq_agent, "unrelated": decline_to_answer}),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
