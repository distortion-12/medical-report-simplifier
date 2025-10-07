Project Title: AI-Powered Medical Report Simplifier (Problem 7)
A brief, one-sentence description of the project.

Setup Instructions
Provide clear steps to run your project.

Ensure Python 3.8+ and Google's Tesseract OCR engine are installed.

Clone the repository.

Install dependencies: pip install -r requirements.txt

Run the server: uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000.

Architecture Explanation
Describe the backend architecture you built.

Framework: The application uses FastAPI, a modern, high-performance Python web framework.

Service Layer: The core logic is separated into a modular service layer:

ocr_service.py: Handles image-to-text conversion.

parsing_service.py: Contains the logic for extracting and normalizing data from the text.

validation_service.py: Implements guardrails to prevent AI hallucinations.

Data Models: Pydantic models are used in schemas.py to enforce strict, validated JSON structures for all API responses, ensuring correctness.

API Usage Examples
Show exactly how to test your endpoint.

cURL (using Command Prompt):

DOS

curl -X POST -F "file=@report.txt" http://127.0.0.1:8000/process-report/
Postman:

Set the method to POST and the URL to http://127.0.0.1:8000/process-report/.

Go to Body -> form-data.

Set the Key as file, change the type from "Text" to "File", and select your report.txt or an image file.

Click Send.

AI Prompts Used and Refinements
Since we mocked the AI, describe the prompts you would use with a real LLM.

Initial Prompt (for data extraction):

"From the text below, extract each full medical test result as a separate string. Text: "{raw_text}". Respond with a JSON array of strings ONLY."

Refinement: The initial prompt was refined to ensure the AI did not add conversational text and returned only the raw data, which is then handled by the application logic.