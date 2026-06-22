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
from google.adk.events.event_actions import EventActions
from google.adk.agents.context import Context
from app.security.input_guards import check_input_safety

def route_query(ctx: Context, node_input: dict) -> Event:
    """Routes execution flows based on classification and verifies input safety boundaries."""
    # Extract original query text
    user_text = ""
    if ctx.user_content and ctx.user_content.parts:
        user_text = "".join(part.text for part in ctx.user_content.parts if part.text)

    # Layer 4 Boundary: Input Safety Scan
    if not check_input_safety(user_text):
        # Force route to decline node if injection is suspected
        return Event(output=user_text, actions=EventActions(route="unrelated"))

    # Intent routing
    is_shipping = node_input.get("is_shipping_related", False)
    if is_shipping:
        return Event(output=user_text, actions=EventActions(route="shipping"))
    else:
        return Event(output=user_text, actions=EventActions(route="unrelated"))
