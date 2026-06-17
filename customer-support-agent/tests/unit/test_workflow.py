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

import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types

from app import app


@pytest.mark.asyncio
async def test_shipping_query() -> None:
    """Verify routing and answering for shipping queries."""
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="app", user_id="test_user"
    )

    outputs = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="What are the shipping rates to New York?")
            ],
        ),
    ):
        if event.content is not None and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    outputs.append(part.text)

    assert len(outputs) > 0
    # The first output might be the classification from classifier_agent: '{"is_shipping_related": true}'
    # The second output should be the answer from the shipping FAQ agent.
    # We verify that we got a non-decline customer support answer.
    has_faq_answer = any(
        "apologize" not in text and "is_shipping_related" not in text
        for text in outputs
    )
    assert has_faq_answer


@pytest.mark.asyncio
async def test_unrelated_query() -> None:
    """Verify routing and polite declining for unrelated queries."""
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="app", user_id="test_user"
    )

    outputs = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Write a Python function to sort a list.")
            ],
        ),
    ):
        if event.content is not None and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    outputs.append(part.text)

    assert len(outputs) > 0
    # The decline node outputs a deterministic string which we can verify.
    has_decline_msg = any(
        "I apologize, but I can only assist with shipping-related queries" in text
        for text in outputs
    )
    assert has_decline_msg
