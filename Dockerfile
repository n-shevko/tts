FROM ghcr.io/coqui-ai/tts

RUN mkdir /tts_models
COPY . .
ENV COQUI_TOS_AGREED="1"
ENV TTS_HOME="/tts_models"
ENV XDG_DATA_HOME="/tts_models"
RUN pip3 install pydub==0.25.1
ENTRYPOINT ["python3", "server.py"]