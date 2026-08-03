import yaml
from .base import BaseExtractor

class YAMLExtractor(BaseExtractor):
    def extract(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            try:
                # Basic validation
                yaml.safe_load(f)
                f.seek(0)
                return f.read()
            except yaml.YAMLError:
                f.seek(0)
                return f.read()
