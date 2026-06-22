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
from google.genai import types

def decline_to_answer(ctx: Context) -> Event:
    """Politely decline to answer non-shipping queries."""
    decline_text = (
        "I apologize, but I can only assist with shipping-related queries like rates, "
        "tracking, delivery, and returns. How can I help you with your shipment today?"
    )
    return Event(
        content=types.Content(
            role="model", parts=[types.Part.from_text(text=decline_text)]
        ),
        output=decline_text,
    )
