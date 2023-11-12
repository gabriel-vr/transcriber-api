from .. import ITranscribeService, Transcription, ITranscribe
from services.diarization import Speech, IDiarize
from services.audio import IAudioHandler
from .whisperInterfaceToService import WhisperLocal
import math

from tempfile import NamedTemporaryFile, _TemporaryFileWrapper


class WhisperTranscriptionService(ITranscribeService):
    diarizer: IDiarize
    transcriber: ITranscribe
    segmentedFile: _TemporaryFileWrapper
    audioCut: _TemporaryFileWrapper
    spacermillisecs: int 
    audioHandler: IAudioHandler

    def __init__(self,*, 
                 transcriber: ITranscribe =WhisperLocal(model='medium', device='cpu'), 
                 diarizer: IDiarize, 
                 audioHandler: IAudioHandler,
                 spacermillisecs: int= 1000) -> None:
        
        super().__init__()
        
        self.transcriber = transcriber
        self.diarizer = diarizer
        self.segmentedFile = NamedTemporaryFile(dir='./temp/',suffix='.wav')
        self.audioCut = NamedTemporaryFile(dir='./temp/',suffix='.wav')
        self.spacermillisecs = spacermillisecs
        self.audioHandler = audioHandler


    def __del__(self):
        self.segmentedFile.close()
        self.audioCut.close()


    def transcribeAudio(self, path: str, *args, **kwargs) -> [Speech]:


        #cut audio in x milliseconds
        self.audioHandler.cutAudio(path, self.audioCut.name, 0, 60 * 1000 * 0.2)


        self.audioHandler.prependToAudio(self.audioCut.name, self.spacermillisecs)

        #realizes diarization
        speeches = self.diarizer.diarize(self.audioCut.name)
        print([speech.toDICT() for speech in speeches])
        

        #get segments where speeches begin in the segmented audio
        segments = self.audioHandler.addTimeBetweenSpeeches(self.audioCut.name, self.segmentedFile.name, self.spacermillisecs, speeches)


        result = self.transcriber.transcribeAudio(self.segmentedFile.name)

        #add text to speeches object
        self.attachTranscriptionToSpeech(result, speeches, segments, self.spacermillisecs)

        #the speeches start and end contain the spacer added at the beginning of the audio
        self.diarizer.addTimeToSpeeches(speeches, -self.spacermillisecs)


        return speeches
    
    
    
    
    def attachTranscriptionToSpeech(self, transcription: [Transcription], speeches: [Speech], segments: [int], spacer: int = 0):
        segmentIdx = 0
        transcribedSegmentIdx = 0
        for segmentIdx in range(len(segments)):
            
            endTime = segments[segmentIdx + 1] - spacer if  segmentIdx < len(segments) - 1 else math.inf
            text = []
            
            while(transcribedSegmentIdx < len(transcription) and int(transcription[transcribedSegmentIdx].start * 1000) <= endTime):
                text.append(transcription[transcribedSegmentIdx].text)
                transcribedSegmentIdx+=1
            speeches[segmentIdx].text = "".join(text)

        