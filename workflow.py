from query_engine import run_query
from pdf_pipeline import process_pdf_to_chunks
from embedding_pipeline import embed_and_store_chunks
import json
# from llm_utils import ask_llm   <- will add this next

def main_workflow(pdf_path):
    # pdf_path = r"C:\Users\murha\OneDrive\Desktop\CA foundation material\cpu1-2merged.pdf"
    json_path = "./chunks.json"
    embedding_path = "./chunk_embeddings.npy"

    process_pdf_to_chunks(pdf_path, json_path)
    embed_and_store_chunks(json_path, embedding_path)

    user_query = """Cryptography & Encryption.
    You are an expert quiz question generator. Your task is to create a list of 10 quiz questions, along with their options and correct answers.

**The output MUST be a valid JSON array of question objects.**

Each question object in the array MUST adhere to the following strict schema:

-   **`id`**: (String) A unique identifier for the question (e.g., "q1", "q2").
-   **`questionText`**: (String) The actual question text.
-   **`questionType`**: (String) The type of question. Allowed values are "multiple-choice", "text-input", "multiple-select", or "true-false".
-   **`options`**: (Array of Objects, *optional*) An array of possible answer options for "multiple-choice", "multiple-select", and "true-false" question types. Each option object MUST have:
    -   **`id`**: (String) A unique identifier for the option (e.g., "opt1").
    -   **`text`**: (String) The text of the option.
-   **`correctAnswerId`**: (String, *optional*) For "multiple-choice" and "true-false" questions, this is the `id` of the single correct option.
-   **`correctAnswer`**: (String, *optional*) For "text-input" questions, this is the exact correct answer.
-   **`correctAnswerIds`**: (Array of Strings, *optional*) For "multiple-select" questions, this is an array of `id`s of all correct options.
-   **`explanation`**: (String, *optional*) A brief explanation for the correct answer.

**IMPORTANT: Ensure all string values are properly escaped for JSON (e.g., double quotes within a string are escaped with a backslash `\"`).**

Here is an example of the desired JSON format:

```json
[
  {
    "id": "q1",
    "questionText": "What is the capital of France?",
    "questionType": "multiple-choice",
    "options": [
      { "id": "opt1", "text": "Berlin" },
      { "id": "opt2", "text": "Madrid" },
      { "id": "opt3", "text": "Paris" },
      { "id": "opt4", "text": "Rome" }
    ],
    "correctAnswerId": "opt3",
    "explanation": "Paris is the capital and most populous city of France."
  },
  {
    "id": "q2",
    "questionText": "Which planet is known as the Red Planet?",
    "questionType": "multiple-choice",
    "options": [
      { "id": "opt5", "text": "Earth" },
      { "id": "opt6", "text": "Mars" },
      { "id": "opt7", "text": "Jupiter" },
      { "id": "opt8", "text": "Venus" }
    ],
    "correctAnswerId": "opt6",
    "explanation": "Mars is often called the Red Planet because of its reddish appearance, caused by iron oxide (rust) on its surface."
  }
]"""
    top_context = run_query(user_query, json_path, embedding_path, top_k=3)

    # Now send to LLM
    from llm_utils import ask_gemini  # example for Gemini
    response = ask_gemini(user_query, top_context)
    
    # print("LLM Answer:\n", response)
    # print(response[7:-4])
    questions = response[7:-4]
    res_json = json.loads(questions)  # Validate JSON format
    print("Response JSON:\n", res_json)
    return res_json