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

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from app.prompts.system_prompts import CLASSIFIER_INSTRUCTION

class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user query is about shipping (rates, tracking, delivery, returns). False otherwise."
    )

classifier_agent = LlmAgent(
    name="classifier_agent",
    model="gemini-2.5-flash",
    instruction=CLASSIFIER_INSTRUCTION,
    output_schema=Classification,
    output_key="classification",
)
