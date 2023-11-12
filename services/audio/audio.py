import subprocess
from ..diarization import Speech

import abc


class IAudioHandler(abc.ABC):
    @staticmethod
    def convertFileFromWebOrLocalToAudio(url: str, output: str) -> None:
        subprocess.run(['yt-dlp',
                        '--enable-file-urls',
                        '--force-overwrites', 
                        '-xv', 
                        '--ffmpeg-location',  
                        '/bin',  
                        '--audio-format',  
                        'wav',   
                        '-o',  
                        output,  
                        '--',  
                        url])

    @staticmethod
    @abc.abstractmethod
    def cutAudio(path: str, pathDest: str, begin: int, end: int) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def prependToAudio(path: str,time: int) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def addTimeBetweenSpeeches(path: str, pathOutput: str, time: int, speeches: [Speech])-> [int]:
        pass

    


