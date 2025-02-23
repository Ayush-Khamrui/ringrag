---

# RinggRag

This is a **Flask-based RAG Project** that enables **document upload to AWS S3** and **question answering (QA) retrieval** based on stored documents. The project follows a modular structure with separate concerns for models, routes, and services.

---

## 📁 Folder Structure

```
📦 app
 ┣ 📂 models
 ┃ ┣ 📜 __init__.py          # Initializes models module
 ┃ ┣ 📜 embedding.py         # Handles embedding-related operations (Embedding model)
 ┃ ┣ 📜 generation.py        # Generates responses from models. LLM model defined
 ┃ ┣ 📜 retrieval.py         # Retrieves relevant documents based on queries (VectorDB & Retriever)
 ┃ ┗ 📜 splitter.py          # Splits documents for processing (Chunking)
 ┣ 📂 routes
 ┃ ┣ 📜 __init__.py          # Initializes routes module
 ┃ ┗ 📜 api_routes.py        # Defines API endpoints for document upload & Q&A
 ┣ 📂 services
 ┃ ┣ 📜 __init__.py          # Initializes services module
 ┃ ┣ 📜 document_service.py  # Handles document operations with AWS S3
 ┃ ┗ 📜 query_service.py     # Processes user questions and retrieves answers
 ┣ 📜 .env                   # Environment variables (not included in repo)
 ┣ 📜 config.py              # Configuration settings (e.g., AWS credentials)
 ┣ 📜 main.py                # Entry point to start the Flask application
 ┣ 📜 requirements.txt       # List of dependencies
 ┣ 📜 .gitignore             # Files to ignore in version control
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/your-repo/flask-rag-api.git](https://github.com/Ayush-Khamrui/ringrag.git)
cd app
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables  
Create a `.env` file in the root directory and add:
```
GOOGLE_API_KEY=your_google_ai_studio_api_key
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

---

## 🔥 Running the Application
```bash
python main.py
```
By default, the server will run at **http://127.0.0.1:5000**.

---

## 🛠 API Endpoints

### 1️⃣ Upload a Document to AWS S3
#### **POST** `/upload`
**Description:** Uploads/updates a file to an S3 bucket.  
**Allowed File Types:** `pdf`, `docx`, `json`, `txt`

**Request Example (Multipart Form-Data):**
```bash
curl -X POST http://127.0.0.1:5000/upload \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "message": "File successfully uploaded in S3"
}
```

---

### 2️⃣ Ask a Question
#### **POST** `/ask`
**Description:** Retrieves answers from stored documents.  

**Request Example (JSON):**
```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d '{
        "question": "What is the content of the document?",
        "title": "document.pdf" <optional>
      }'
```

**Response Example:**
```json
{
  "answer": "The document discusses Flask-based RAG applications."
}
```

---

## 📝 Notes:
- Ensure AWS & Google credentials are configured correctly in **.env**.
- The **document_service.py** handles document uploads and retrieval from S3.
- The **query_service.py** processes user queries and retrieves answers using an NLP pipeline.

---

## 👨‍💻 Contributing
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a **Pull Request**

---

---
