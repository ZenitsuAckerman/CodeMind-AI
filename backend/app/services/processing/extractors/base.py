from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    Abstract base class for all text extractors.
    """
    @abstractmethod
    def extract(self, file_path: str) -> str:
        """
        Extracts plain text from the given file path.
        """
        pass
