import pymupdf
from .base import BaseExtractor

class PDFExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        doc = pymupdf.open(file_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)
