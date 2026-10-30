import json
import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from pypdf import PdfReader
from docx import Document


# --------------------------------------------------
# 1. LOAD API KEY AND CREATE GEMINI CLIENT
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to the .env file."
    )

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.8-flash"

# --------------------------------------------------
# 2. COMMON GEMINI FUNCTION
# --------------------------------------------------

def generate_json(system_prompt: str, user_prompt: str) -> dict:
    """Send a prompt to Gemini and return the JSON response as a dictionary."""

    response = client.models.generate_content(
        model=MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0,
        ),
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini did not return valid JSON:\n{response.text}"
        ) from exc


# --------------------------------------------------
# 3. JOB DESCRIPTION
# --------------------------------------------------

job_description = """
Description
Do you want to solve real customer problems through innovative technology?
Do you enjoy working on scalable services in a collaborative team environment?
Do you want to see your code directly impact millions of customers worldwide?

At Amazon, we hire the best minds in technology to innovate and build on behalf
of our customers. Customer obsession is part of our company DNA, which has made
us one of the world's most beloved brands.

Our Software Development Engineers (SDEs) use modern technology to solve complex
problems while seeing their work's impact first-hand. The challenges SDEs solve
at Amazon are meaningful and influence millions of customers, sellers, and
products globally. We seek individuals passionate about creating new products,
features, and services while managing ambiguity in an environment where
development cycles are measured in weeks, not years.

At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the
entire lifecycle of your code - from design through deployment and ongoing
operations. This ownership mindset, combined with our commitment to operational
excellence, ensures we deliver the highest quality solutions for our customers.

We're looking for curious minds who think big and want to define tomorrow's
technology. At Amazon, you'll grow into the high-impact engineer you know you
can be, supported by a culture of learning and mentorship. Every day brings
exciting new challenges and opportunities for personal growth.

Key job responsibilities
- Collaborate and communicate effectively with experienced cross-disciplinary
  Amazonians to design, build, and operate innovative products and services.
- Design and develop scalable solutions using cloud-native architectures and
  microservices in a large distributed computing environment.
- Participate in code reviews and contribute to technical documentation.
- Build and maintain resilient distributed systems that are scalable,
  fault-tolerant, and cost-effective.
- Leverage and contribute to the development of GenAI and AI-powered tools.
- Write clean, maintainable code following best practices and design patterns.
- Work in an agile environment practicing CI/CD principles.
- Demonstrate operational excellence through monitoring, troubleshooting,
  and resolving production issues.

Basic Qualifications
- Experience with at least one general-purpose programming language such as
  Java, Python, C++, C#, Go, Rust, or TypeScript.
- Experience with data structure implementation, basic algorithm development,
  and/or object-oriented design principles.
- Currently has, or is in the process of obtaining, a bachelor's degree in
  Computer Science, Computer Engineering, Data Science, Information Systems,
  or a related STEM field.
- Must be 18 years of age or older.

Preferred Qualifications
- Previous technical internship(s) or demonstrated project experience.
- Experience with AI tools for development productivity, cloud platforms
  (preferably AWS), databases (SQL and NoSQL), open-source contributions,
  version control systems, debugging, and troubleshooting.
- Ability to learn and adapt to new technologies quickly.
- Basic understanding of software development lifecycle (SDLC).
- Strong problem-solving, analytical, written, and verbal communication skills.
"""


# --------------------------------------------------
# 4. PYDANTIC MODELS
# --------------------------------------------------

class JobD(BaseModel):
    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience: float | None = None
    education_requirements: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = Field(default_factory=list)
    experiences: list[Experience] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    score: float
    details: dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------
# 5. EXTRACT STRUCTURED DATA FROM JOB DESCRIPTION
# --------------------------------------------------

def parse_job_description(description: str) -> JobD:
    system_prompt = f"""
You are an expert HR assistant.
Extract structured information from the job description.
Return only valid JSON matching this Pydantic schema:

{json.dumps(JobD.model_json_schema(), indent=2)}

Rules:
- Do not return the schema itself.
- Extract only information supported by the job description.
- If minimum experience is not mentioned, use null.
- If information for a list is missing, use an empty list.
- Do not invent information.
"""

    data = generate_json(system_prompt, description)
    return JobD(**data)


# --------------------------------------------------
# 6. PARSE RESUME
# --------------------------------------------------

def parse_resume(resume_text: str) -> Resume:
    system_prompt = f"""
You are an expert resume parser.
Extract information from the resume based on its meaning,
not only exact section headings.

For example, Experience, Professional Experience, Work History,
Employment, and Internships may all contain relevant experience.
Skills may appear in the skills section, experience, internships,
or projects.

Return only valid JSON matching this schema:

{json.dumps(Resume.model_json_schema(), indent=2)}

Rules:
1. Do not invent information.
2. If a value is unavailable, use null.
3. If a list has no information, use an empty list.
4. Include internships inside experiences.
5. Extract skills mentioned across the entire resume.
"""

    data = generate_json(
        system_prompt,
        f"Parse the following resume:\n\n{resume_text}",
    )
    return Resume(**data)


# --------------------------------------------------
# 7. COMPARE RESUME WITH JOB DESCRIPTION
# --------------------------------------------------

def final_score(job: JobD, resume: Resume) -> MatchResult:
    system_prompt = """
You are a careful and fair technical recruiter.
Compare the candidate's resume with the job description.
Return only valid JSON with these fields:
- score: a number from 0 to 100
- details: an object containing candidate_name, matching_skills,
  missing_important_skills, experience_requirement_met, and final_verdict.

Base the score only on evidence in the supplied data.
Do not invent qualifications or experience.
"""

    user_prompt = f"""
JOB DESCRIPTION DATA:
{job.model_dump_json(indent=2)}

CANDIDATE RESUME DATA:
{resume.model_dump_json(indent=2)}

Evaluate:
1. Candidate name.
2. Matching skills.
3. Missing important skills.
4. Whether the experience requirement is met.
5. Overall match percentage from 0 to 100.
6. A short final verdict.
"""

    data = generate_json(system_prompt, user_prompt)

    # Keep the score within the expected range.
    data["score"] = max(0, min(100, float(data["score"])))

    return MatchResult(**data)


# --------------------------------------------------
# 8. READ PDF AND DOCX RESUMES
# --------------------------------------------------

def read_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages_text.append(page_text)

    return "\n".join(pages_text)


def read_docx(file_path: Path) -> str:
    document = Document(str(file_path))
    text_parts = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text_parts.append(cell.text)

    return "\n".join(text_parts)


def read_resume(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(file_path)

    if suffix == ".docx":
        return read_docx(file_path)

    raise ValueError(f"Unsupported resume format: {suffix}")


# --------------------------------------------------
# 9. MAIN PROGRAM
# --------------------------------------------------

def main():
    resume_folder = BASE_DIR / "resumes"

    if not resume_folder.exists():
        raise FileNotFoundError(
            f"Resume folder not found: {resume_folder}\n"
            "Create a folder named 'resumes' beside main.py and add PDF/DOCX files."
        )

    resume_files = [
        path for path in resume_folder.iterdir()
        if path.is_file() and path.suffix.lower() in {".pdf", ".docx"}
    ]

    if not resume_files:
        print("No PDF or DOCX resumes found in the resumes folder.")
        return

    print("\nAnalyzing job description...")
    job = parse_job_description(job_description)

    print("\nExtracted Job Role:", job.role)
    print("Required Skills:", job.required_skills)
    print("Preferred Skills:", job.preferred_skills)
    print("Minimum Experience:", job.minimum_experience)
    print("\nStarting resume matching...\n")

    all_results = []

    for file_path in resume_files:
        print(f"Processing: {file_path.name}")

        try:
            resume_text = read_resume(file_path)

            if not resume_text.strip():
                print("Skipped: No readable text found in this file.\n")
                continue

            parsed_resume = parse_resume(resume_text)

            # Small pause between API requests; this does not guarantee
            # unlimited quota or prevent all rate-limit errors.
            time.sleep(2)

            result = final_score(job, parsed_resume)

            print(f"Candidate: {parsed_resume.name or file_path.stem}")
            print(f"Match Score: {result.score:.1f}%")
            print("Details:", result.details)
            print("-" * 60)

            all_results.append({
                "name": parsed_resume.name or file_path.stem,
                "file": file_path.name,
                "score": result.score,
                "details": result.details,
            })

            time.sleep(2)

        except Exception as error:
            print(f"Could not process {file_path.name}: {error}\n")

    if not all_results:
        print("No resumes could be processed.")
        return

    all_results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True,
    )

    print("\n========== TOP CANDIDATES ==========")
    for candidate in all_results[:2]:
        print(
            f"{candidate['name']} ({candidate['file']}) "
            f"- {candidate['score']:.1f}%"
        )
        print("Details:", candidate["details"])
        print()

    print("\n========== LOWEST MATCHES ==========")
    for candidate in all_results[-2:]:
        print(
            f"{candidate['name']} ({candidate['file']}) "
            f"- {candidate['score']:.1f}%"
        )
        print("Details:", candidate["details"])
        print()

    # Save the complete ranking to a JSON file.
    output_file = BASE_DIR / "match_results.json"
    output_file.write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
