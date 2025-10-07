from typing import List
from app.models.schemas import NormalizedTest

# For verifying every reported test actually appears in the original text.
def validate_no_hallucinations(raw_text: str, normalized_tests: List[NormalizedTest]):
    """
    Ensures that every test reported in the normalized output is mentioned
    in the original raw text to prevent AI hallucination.
    
    Args:
        raw_text: The original text from the report.
        normalized_tests: The list of structured test results from the AI.
        
    Raises:
        ValueError: If a test is found that was not in the raw text.
    """
    raw_text_lower = raw_text.lower()
    for test in normalized_tests:
        if test.name.lower() not in raw_text_lower:
            raise ValueError(f"Hallucinated test detected: '{test.name}' not found in the original report.")