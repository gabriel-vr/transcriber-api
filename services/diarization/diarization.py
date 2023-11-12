import abc
import json

class Speech:
    start: int
    end: int
    speaker: str
    text: str
    

    def __init__(self, *,start: int, end: int, speaker: int, text: str =  "") -> None:
        self.start = start
        self.end = end
        self.speaker = speaker
        self.text = text

    def toDICT(self):
        return {
            "start": self.start,
            "end": self.end,
            "speaker": self.speaker,
            "text": self.text,
        }


class IDiarize(abc.ABC):
    @abc.abstractmethod
    def diarize(self, path: str) -> [Speech]:
        pass

    def addTimeToSpeeches(self, speeches: [Speech], time: int):
        for speech in speeches:
            speech.start += time/1000
            speech.end += time/1000



