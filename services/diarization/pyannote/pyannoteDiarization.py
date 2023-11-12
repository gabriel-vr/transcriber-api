from pyannote.audio import Pipeline

#TODO: Insert use_auth_token
class PyannoteDiarization:
    numberSpeakers: int
    pipeline: Pipeline
    def __init__(self, *, use_auth_token = '', numberSeakers: int = None) -> None:
        self.pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=use_auth_token)
        self.numberSpeakers = numberSeakers
    
    def diarizeAudio(self, path: str):
        dz = self.pipeline(path, num_speakers=self.numberSpeakers)  
        return dz