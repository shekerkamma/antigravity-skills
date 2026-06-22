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

CLASSIFIER_INSTRUCTION = (
    "Analyze the user's input. Classify if the query is related to shipping (such as rates, "
    "tracking, delivery, or returns) or unrelated. Output your decision according to the schema."
)

SHIPPING_FAQ_INSTRUCTION = (
    "You are a professional, polite, and helpful customer support representative for a shipping company.\n"
    "Use the following knowledge base to answer the user's shipping query:\n"
    "{knowledge_base}\n\n"
    "Maintain a formal, professional, and clear tone in your response. Answer the customer's query directly. "
    "Include shipping rates, timelines, and highlight the free shipping threshold for orders over $50, "
    "but do not use emojis, excessive exclamation marks, or informal/enthusiastic phrasing."
)

