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
from google.adk.apps import App

# Import modular components conforming to 9-Layer Architecture
from app.agents.classifier import classifier_agent
from app.agents.router import route_query
from app.agents.faq_responder import shipping_faq_agent
from app.agents.decline import decline_to_answer

# Assemble Workflow Agent
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
