import xml.etree.ElementTree as ET
from .base import BaseExtractor

class XMLExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            try:
                ET.parse(file_path)
                f.seek(0)
                return f.read()
            except ET.ParseError:
                f.seek(0)
                return f.read()
