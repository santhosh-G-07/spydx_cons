import spacy
from pdfminer.high_level import extract_text


nlp = spacy.load("en_core_web_sm")

class ResumeAgent:
    def __init__(self, file_path):
        self.text = extract_text(file_path)
        self.doc = nlp(self.text)

    def extract_name(self):
        for ent in self.doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Unknown"

    def extract_email(self):
        for token in self.doc:
            if "@" in token.text and "." in token.text:
                return token.text
        return "Unknown"

    def extract_skills(self):
        # Dummy keywords — you can expand
        skills = ["python", "django", "sql", "machine learning", "nlp", "tensorflow"]
        found_skills = []
        text_lower = self.text.lower()
        for skill in skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return list(set(found_skills))

    def extract_all(self):
        return {
            "name": self.extract_name(),
            "email": self.extract_email(),
            "skills": self.extract_skills()
        }
