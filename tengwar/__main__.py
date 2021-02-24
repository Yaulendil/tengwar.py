from sys import argv

from . import transcribe


print(*map(transcribe, argv[1:]))
