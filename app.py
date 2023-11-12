from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import torch

from services.audio.audioSegmenter import AudioSegmenterService
from services.transcription.whisper import WhisperTranscriptionService, WhisperLocal, WhisperApi
from services.diarization.pyannote import PyanotteDiarizeService

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


app = Flask(__name__)

@app.route("/")
def hello():
    return "Whisper Hello World!"


@app.route('/whisper', methods=['POST'])
def handler():
    
    #if user sent a file it will be stored here
    temp = NamedTemporaryFile()
    try:
        #verify if user sent an url to a file
        url = request.form.get('url')
        numberSpeakers = int(request.form.get('numberSpeakers'))

        if(numberSpeakers is None):
            abort(400)

        if(url is None):
            if not request.files:
                # If the user didn't submit any files, return a 400 (Bad Request) error.
                abort(400)
            else:
                for filename, handle in request.files.items():
                    handle.save(temp)
                    url = 'file://' + temp.name
                    break



        tempAudio = NamedTemporaryFile(dir='./temp/',suffix='.wav')


        #get file from web or localhost and extract audio
        AudioSegmenterService.convertFileFromWebOrLocalToAudio(url, tempAudio.name)

        

        transcriber = WhisperTranscriptionService(diarizer=PyanotteDiarizeService(numberSpeakers=numberSpeakers), 
                                                  transcriber= WhisperLocal(model='medium', device=DEVICE),#WhisperApi(),
                                                  audioHandler=AudioSegmenterService)
        
        #transcribe audio
        transcription = transcriber.transcribeAudio(tempAudio.name)
        

        temp.close()
        tempAudio.close()

        # This will be automatically converted to JSON.
        return {'results': [speech.toDICT() for speech in transcription]}

    except Exception as e:
        print(str(e))
        abort(500)

    