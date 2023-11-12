
from .pyannoteDiarization import PyannoteDiarization
from ..diarization import IDiarize, Speech

class PyanotteDiarizeService(IDiarize):
    
    def __init__(self, *, numberSpeakers: int) -> None:
        super().__init__()
        self.diarizer = PyannoteDiarization(numberSeakers=numberSpeakers)
    
    

    def diarize(self, path: str) -> [Speech]:
        diarization = self.diarizer.diarizeAudio(path)
        speeches = self.getSpeeches(diarization)
        return speeches
    

    def getSpeeches(self, diarization)-> [Speech]:
        speeches = []
        for speech in list(diarization.itertracks(yield_label = True)):
            start = round(speech[0].start , 3)
            end = round(speech[0].end , 3)
            speaker = speech[2]
            speeches.append(Speech(start=start, end=end, speaker=speaker))
        return speeches
