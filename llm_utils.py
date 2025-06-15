import google.generativeai as genai

def ask_gemini(query: str, context: str) -> str:
    genai.configure(api_key="AIzaSyCSw25UVnth3OO6B24ak8ZcEzN1TDaBBjs")
    model = genai.GenerativeModel(model_name='gemini-2.0-flash')
    response = model.generate_content(f"""generate best reponse to the following question based on the context provided:
{query} {context}""")
    
    print(type(response.text))
    return response.text.strip()



query = """generate a ICAI standard exam 10 MCQs on this topic.
You are an expert quiz question generator. Your task is to create a list of quiz questions, along with their options and correct answers.

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
context = """Accounting provides information that is useful to various stakeholders like investors, creditors, and management. Its objective is to record, classify, and summarize financial transactions to determine profit/loss and financial position. Accounting follows certain qualitative characteristics like reliability, relevance, understandability, and comparability to make the information useful."""
# print(ask_gemini(query, context))
