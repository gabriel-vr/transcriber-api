
import whisper
from .. import Transcription

from .. import Transcription, ITranscribe

import openai

class WhisperLocal(ITranscribe):
    model: whisper.Whisper

    def __init__(self, *, model: str, device: str) -> None:
        super().__init__()
        self.model = whisper.load_model(model, device=device)

    def transcribeAudio(self, path: str, *args, **kwargs) -> [Transcription]:
        result = self.model.transcribe(path)

        transcription = []
        for segment in result['segments']:
            transcription.append(Transcription(start=segment['start'], end=segment['end'], text=segment['text']))

        return transcription
    
#TODO: Insert api_key and organization 
class WhisperApi(ITranscribe):
    model: str
    api_key: str= ''
    organization: str = ''

    def __init__(self, *, model: str='whisper-1') -> None:
        super().__init__()
        self.model = model



    def transcribeAudio(self, path: str, *args, **kwargs) -> [Transcription]:
        file = open(path, 'rb')
        result = openai.Audio.transcribe(self.model, file, self.api_key, organization=self.organization, response_format='verbose_json')
        print(result)
        transcription = []
        for segment in result['segments']:
            transcription.append(Transcription(start=segment['start'], end=segment['end'], text=segment['text']))

        return transcription
