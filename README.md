### 📽 Demo

https://your-video-link.com](https://youtu.be/Ww6a--2WNco

📘 CA Proctor Test Helper
AI-powered quiz generator + real-time exam collaboration tool for CA students and beyond

🚀 Overview
This project allows users to generate multiple-choice questions (MCQs) from study materials (PDFs) using AI, and conduct real-time collaborative exams using Firebase.

✅ Built for CA students, but can be adapted for any subject
✅ Powered by Gemini API, Google Drive, semantic search, and Firebase
✅ Future-proof idea: ready to expand into theory, numerical, and image-based answers

🔍 Key Features
Feature	Description
📥 PDF Upload via Google Drive	Users can upload PDF study materials using a Drive link
🧠 AI MCQ Generator	Embeddings + semantic search + Gemini API generate high-quality MCQs
🔄 Real-Time Exam Sync	Firebase Realtime DB syncs questions across all participants live
🔐 Prompt Engineering	Custom prompt + semantic context ensures relevant questions
🧪 Modular Backend	Built with clean, reusable architecture using Flask
🌐 Frontend	React frontend for uploading, conducting, and managing tests
📸 (Upcoming) Image answer upload for theory/numerical questions	

🛠 Tech Stack
Frontend: React.js

Backend: Flask (Python)

AI API: Gemini 2.0 Flash

Database: Firebase Realtime DB

PDF + NLP: PyMuPDF, NLTK, and sentence transformers

Authentication: Google Drive API for PDF input

📊 How It Works
User uploads Google Drive PDF link

PDF is downloaded and parsed into clean text

Text is chunked by heading structure (chapter/subchapter)

Chunks are embedded, and semantic search fetches the most relevant parts

User asks a question → Top 3 chunks + query sent to Gemini

AI returns JSON of MCQs → stored and synced with all participants using Firebase

📈 Real-World Use Case
Built originally for a CA student’s need, this project solves a real problem:
Creating subject-relevant MCQs from study materials instantly and interactively.

Imagine replacing manual question setting with this system — scalable, accurate, smart.

💡 Future Improvements
📸 Upload handwritten answers using mobile → send image to Gemini for evaluation

✍️ Add support for theory and numerical questions

📤 Export test results to PDF/Excel

👩‍🏫 Add admin dashboard for teachers/coaches

🤝 Collaboration & Contribution
Open to collaborators! Whether you're a CA educator, student, or developer, feel free to create issues or submit PRs.

👨‍💻 Author
S. Murali Mohan
Full Stack Developer | Passionate about AI, Education & Scalable Systems
🔗 [LinkedIn](https://www.linkedin.com/in/murali-mohan-662245259/)
🛠️ “The more you know, the more you realize you know nothing.”
