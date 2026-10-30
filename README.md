# 🤖 Job-Match-AI

### AI-Powered Resume and Job Description Matching System

Job-Match-AI is an AI-powered application that analyzes job descriptions and candidate resumes to identify the most suitable candidates for a given job role.

Built using **Python, Google Gemini API, and Pydantic**, this project extracts important information from job descriptions and resumes, evaluates candidate skills and experience, and generates candidate match scores to simplify the recruitment process.

---

## 🚀 Features

* **AI-Powered Job Description Analysis:** Extracts job roles, required skills, preferred skills, experience requirements, education, and responsibilities.
* **Resume Parsing:** Extracts candidate information from PDF and DOCX files.
* **Skill Matching:** Compares candidate skills with job requirements.
* **Experience Analysis:** Evaluates candidate experience against the minimum required experience.
* **Candidate Scoring:** Generates AI-based candidate matching scores.
* **Candidate Ranking:** Ranks candidates according to their matching scores.
* **Structured Output:** Uses Pydantic models to maintain structured and validated data.
* **JSON Export:** Saves candidate matching results into a JSON file.

---

## 🛠️ Tech Stack

| Technology        | Purpose                                |
| ----------------- | -------------------------------------- |
| Python            | Core programming language              |
| Google Gemini API | AI-powered analysis and matching       |
| Pydantic          | Data validation and structured outputs |
| Google GenAI SDK  | Gemini API integration                 |
| PyPDF             | Extracting text from PDF resumes       |
| python-docx       | Extracting text from DOCX resumes      |
| python-dotenv     | Managing environment variables         |

---

## 📂 Project Structure

```text
Job-Match-AI/
│
├── mmpy.py
├── .env
├── .gitignore
├── requirements.txt
│
├── resumes/
│   ├── resume1.pdf
│   ├── resume2.pdf
│   └── resume3.docx
│
└── match_results.json
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Premchougule1008/Job-Match-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd Job-Match-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively, install the packages directly:

```bash
pip install google-genai python-dotenv pydantic pypdf python-docx
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

**Important:** Never upload your `.env` file or expose your API key on GitHub.

---

## 📄 Add Resumes

Create a folder named `resumes` in the project directory.

Add candidate resumes in either of these formats:

* PDF (`.pdf`)
* Word Document (`.docx`)

The application processes the resumes from this folder.

---

## ▶️ Run the Project

Execute the following command:

```bash
python mmpy.py
```

The application will:

1. Analyze the job description using Gemini.
2. Extract job requirements.
3. Read candidate resumes.
4. Extract candidate information.
5. Evaluate candidate-job compatibility.
6. Generate candidate matching scores.
7. Rank candidates based on their scores.
8. Save the results in `match_results.json`.

---

## 📊 Output

The application generates a `match_results.json` file containing structured candidate matching information.

The results include extracted candidate details and matching scores.

Candidates are ranked according to their compatibility with the job description.

---

## 🧠 How It Works

```text
       Job Description
              |
              v
     Google Gemini API
              |
              v
    Extract Job Requirements
              |
              v
       Candidate Resumes
         (PDF / DOCX)
              |
              v
       Resume Parsing
              |
              v
      Candidate Analysis
              |
              v
       Skill & Experience
           Matching
              |
              v
       Candidate Scoring
              |
              v
      Candidate Ranking
              |
              v
       JSON Results
```

---

## 🔮 Future Scope

* Develop a web-based interface using Streamlit or FastAPI.
* Add support for multiple job descriptions.
* Implement advanced semantic skill matching.
* Add candidate filtering and search functionality.
* Generate detailed candidate evaluation reports.
* Integrate a database for storing candidate profiles.

---

## ⚠️ Limitations

* Scanned or image-only PDF resumes may require OCR for text extraction.
* Matching scores are AI-generated estimates and should not be treated as definitive hiring decisions.
* Results depend on the quality and completeness of the provided resumes and job descriptions.
* Gemini API usage is subject to applicable API quotas and rate limits.

---

## 👨‍💻 Author

**Prem Chougule**

B.Tech – Artificial Intelligence and Data Science

* GitHub: [@Premchougule1008](https://github.com/Premchougule1008)

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!

