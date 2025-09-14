import os
import pdfplumber
from docx import Document
import spacy
import re

# Load SpaCy English model once when utils.py is loaded
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file_path):
    """Extract full text from a PDF file using pdfplumber."""
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text


def extract_text_from_docx(file_path):
    """Extract plain text from a DOCX file using python-docx."""
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_text_from_resume(file_path):
    """
    Extract text from a resume file based on its extension.
    Supports PDF (via pdfplumber) and DOCX.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        # Could add support for other formats if required
        return ''


def extract_projects_section(text):
    """
    Extract the 'Projects' section from the resume text.

    Looks for section headers like "Projects", "Professional Projects", or "Relevant Projects",
    and grabs text until the next section header (assumed to be a line starting with a capitalized word followed by colon)
    or end of document.

    Returns the raw text of the projects section for further parsing.
    """
    pattern = re.compile(
        r'(Projects|Professional Projects|Relevant Projects)(.*?)(\n[A-Z][a-zA-Z ]*?:|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(text)
    if match:
        # Group 2 contains the projects section text
        projects_text = match.group(2).strip()
        return projects_text
    return ''


def parse_projects(projects_text):
    """
    Parse the projects text section line-by-line to extract individual projects.

    Assumptions:
    - Each project is separated by a newline.
    - Project name and description separated by colon ':' or dash '-'.
    - Lines without separators are treated as project names with empty description.
    """
    projects = []
    lines = projects_text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Try to split with colon or dash separators
        if ':' in line:
            name, description = line.split(':', 1)
        elif '-' in line:
            name, description = line.split('-', 1)
        else:
            name = line
            description = ''

        projects.append({
            'name': name.strip(),
            'description': description.strip(),
        })

    return projects


def parse_projects_nlp(text):
    """
    End-to-end parsing function: extract Projects section from full text,
    then parse individual projects using simple rules.

    This is the main function to call in your views for project extraction.
    """
    projects_section = extract_projects_section(text)
    if not projects_section:
        return []  # no projects section found

    projects = parse_projects(projects_section)
    return projects
