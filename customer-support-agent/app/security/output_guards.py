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

import re

def scrub_pii_and_placeholders(text: str) -> str:
    """
    Scrub PII (like emails) and detect/flag unresolved placeholder brackets in model responses.
    
    Args:
        text: Raw generated output text from the model.
        
    Returns:
        Cleaned and verified text.
    """
    # Simple email pattern scrubbing
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    clean_text = re.sub(email_pattern, "[EMAIL_REDACTED]", text)
    
    # Placeholder warning
    placeholder_pattern = r'\[(?:Your|Insert|Placeholder)[^\]]*\]'
    if re.search(placeholder_pattern, clean_text, re.IGNORECASE):
        clean_text = re.sub(placeholder_pattern, "[INFO_REDACTED]", clean_text)
        
    return clean_text
