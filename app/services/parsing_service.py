import re
from typing import List, Dict, Any
from app.models.schemas import NormalizedTest, ReferenceRange, RawExtractionResponse

REFERENCE_RANGES = {
    "Hemoglobin": {"low": 12.0, "high": 15.0, "unit": "g/dL"},
    "WBC": {"low": 4000, "high": 11000, "unit": "/uL"}
}

EXPLANATIONS = {
    "Hemoglobin": {
        "low": "A low hemoglobin level may suggest anemia, which can cause fatigue and weakness.",
        "high": "Elevated hemoglobin can be a sign of dehydration or other underlying conditions that affect red blood cell count."
    },
    "WBC": {
        "low": "A low white blood cell count can indicate a compromised immune system, making one more susceptible to infections.",
        "high": "A high white blood cell count is often a sign that the body is fighting an infection."
    }
}

def extract_raw_tests(raw_text: str) -> RawExtractionResponse:
    """
    Simulates AI-powered raw text extraction and confidence scoring.
    """
    pattern = re.compile(r"(\w+\s+[\d.]+\s+[a-zA-Z\/]+\s+\([^)]+\))")
    matches = pattern.findall(raw_text)
    
    confidence = min(0.85 + (len(matches) * 0.05), 1.0) if matches else 0.5
    
    return RawExtractionResponse(tests_raw=matches, confidence=round(confidence, 2))

def extract_and_normalize_tests(raw_text: str) -> tuple[List[NormalizedTest], float]:
    """
    Dynamically normalizes tests and correctly calculates the status based on reference ranges.
    """
    normalized_tests = []
    
    pattern = re.compile(r"(\w+)\s+([\d.]+)\s+([a-zA-Z\/]+)\s+\(([^)]+)\)")
    matches = pattern.findall(raw_text)
    
    known_tests_count = 0
    for match in matches:
        name, value_str, unit, _ = match  # We ignore the status from the text
        value = float(value_str)

        if name in REFERENCE_RANGES:
            known_tests_count += 1
            ref = REFERENCE_RANGES[name]
            
            # **Correctly determine the status based on the value**
            if value < ref["low"]:
                determined_status = "low"
            elif value > ref["high"]:
                determined_status = "high"
            else:
                determined_status = "normal"

            normalized_tests.append(NormalizedTest(
                name=name,
                value=value,
                unit=unit,
                status=determined_status,
                ref_range=ReferenceRange(low=ref["low"], high=ref["high"])
            ))

    normalization_confidence = (known_tests_count / len(matches)) * 0.9 if matches else 0.0
    
    return normalized_tests, round(normalization_confidence, 2)

def generate_patient_summary(tests: List[NormalizedTest]) -> Dict[str, Any]:
    """
    Simulates an AI generating a natural language summary and explanations.
    """
    abnormal_tests = [test for test in tests if test.status != "normal"]
    
    if not abnormal_tests:
        summary = "All test results appear to be within the standard normal ranges."
        explanations = []
    else:
        findings = [f"a {test.status} {test.name} level" for test in abnormal_tests]
        if len(findings) > 1:
            summary = f"The key findings from your report are {', '.join(findings[:-1])} and {findings[-1]}."
        else:
            summary = f"The key finding from your report is {findings[0]}."

        explanations = [EXPLANATIONS[test.name][test.status] for test in abnormal_tests if test.name in EXPLANATIONS and test.status in EXPLANATIONS[test.name]]

    return {"summary": summary, "explanations": explanations}