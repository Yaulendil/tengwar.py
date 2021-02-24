from ._base import Transcriber
from .quenya import TranscriberQuenya


def transcribe(word: str, *, xscr: Transcriber = TranscriberQuenya()) -> str:
    return xscr.transcribe(word.casefold())
