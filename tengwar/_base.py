from abc import ABC, abstractmethod

__all__ = "Transcriber",


class Transcriber(ABC):
    @abstractmethod
    def transcribe(self, text: str) -> str: ...
