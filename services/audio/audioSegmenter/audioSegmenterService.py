
from .. import IAudioHandler
from pydub import AudioSegment

from services.diarization import Speech

class AudioSegmenterService(IAudioHandler):
    
    @staticmethod
    def cutAudio(path: str, pathDest: str, begin: int, end: int) -> None:
        newAudio = AudioSegment.from_wav(path)
        a = newAudio[begin:end]
        a.export(pathDest, format="wav") 

    @staticmethod
    def prependToAudio(path: str,time: int) -> None:
        audio = AudioSegment.from_wav(path)
        spacer = AudioSegment.silent(duration=time)
        audio = spacer.append(audio, crossfade=0)
        audio.export(path, format='wav')


    @staticmethod
    def addTimeBetweenSpeeches(path: str, pathOutput: str, time: int, speeches: [Speech])-> [int]:
        segments = []
        spacer = AudioSegment.silent(duration=time)
        sounds = spacer
        audio = AudioSegment.from_wav(path)

        for speech in speeches:
            start = speech.start
            end =  speech.end
            
            segments.append(len(sounds))
            sounds = sounds.append(audio[start*1000:end*1000], crossfade=0)
            sounds = sounds.append(spacer, crossfade=0)

            sounds.export(pathOutput, format="wav") #Exports to a wav file in the current path.
        return segments

