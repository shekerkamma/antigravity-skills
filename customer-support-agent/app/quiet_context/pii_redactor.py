import re
from typing import Dict, Tuple

class PIIRedactor:
    """
    PII Redactor handles compliance and privacy requirements (GDPR/SOX) by
    redacting sensitive information before it reaches LLM APIs.
    It supports masking and mapping for downstream reconstruction if needed.
    """
    def __init__(self):
        # Patterns for common PII
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b"
        }

    def redact(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Redacts PII from text and returns the redacted text and a translation map.
        """
        redacted_text = text
        mapping = {}
        counter = 1

        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, redacted_text)
            # Remove duplicates to avoid redundant replacement
            for match in set(matches):
                placeholder = f"[{label}_{counter}]"
                mapping[placeholder] = match
                redacted_text = redacted_text.replace(match, placeholder)
                counter += 1

        return redacted_text, mapping

    def restore(self, redacted_text: str, mapping: Dict[str, str]) -> str:
        """
        Restores the redacted PII using the mapping.
        """
        restored_text = redacted_text
        for placeholder, original in mapping.items():
            restored_text = restored_text.replace(placeholder, original)
        return restored_text
