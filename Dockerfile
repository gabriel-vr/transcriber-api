FROM python:3.8-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install git -y
#RUN pip install --upgrade pip

#RUN pip install  https://github.com/pyannote/pyannote-audio/archive/refs/heads/develop.zip
#RUN pip install -U yt-dlp
#RUN wget -O - -q  https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz | xz -qdc| tar -x
#RUN pip install pydub
#RUN pip install   pyannote.audio

RUN pip3 install -r requirements.txt

RUN pip3 install "git+https://github.com/openai/whisper.git" 
RUN apt-get install -y ffmpeg

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]