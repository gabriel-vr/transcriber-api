import abc

from ..diarization import Speech

class Transcription:
    start: float
    end: float
    text: str

    def __init__(self, *, start: float, end: float, text: str) -> None:
        self.start = start
        self.end = end
        self.text = text 
    
    def __str__(self) -> str:
        return str({'start': self.start, 'end': self.end, 'text': self.text})

class ITranscribe(abc.ABC):
    @abc.abstractmethod
    def transcribeAudio(self, path: str, *args, **kwargs) -> [Transcription]:
        pass


class ITranscribeService(abc.ABC):
    transcriber: ITranscribe

    @abc.abstractmethod
    def transcribeAudio(self, path: str, *args, **kwargs) -> [Speech]:
        pass




    


