from typing import Type
from .base import BaseExtractor
from .pdf_extractor import PDFExtractor
from .docx_extractor import DOCXExtractor
from .text_extractor import TextExtractor
from .yaml_extractor import YAMLExtractor
from .xml_extractor import XMLExtractor

class ExtractorFactory:
    """
    Factory for obtaining the appropriate text extractor based on file extension.
    """
    
    _extractors = {
        ".pdf": PDFExtractor,
        ".docx": DOCXExtractor,
        ".txt": TextExtractor,
        ".md": TextExtractor,
        ".java": TextExtractor,
        ".py": TextExtractor,
        ".js": TextExtractor,
        ".ts": TextExtractor,
        ".json": TextExtractor,
        ".yaml": YAMLExtractor,
        ".yml": YAMLExtractor,
        ".xml": XMLExtractor,
    }

    @classmethod
    def get_extractor(cls, extension: str) -> BaseExtractor:
        ext = extension.lower()
        extractor_class = cls._extractors.get(ext)
        if not extractor_class:
            raise ValueError(f"No extractor found for extension: {ext}")
        return extractor_class()
