import docx
from .base import BaseExtractor

class DOCXExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
