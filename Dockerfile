FROM ghcr.io/coqui-ai/tts-cpu

RUN mkdir /tts_models
COPY server.py .
ENV COQUI_TOS_AGREED="1"
ENV TTS_HOME="/tts_models"
ENV XDG_DATA_HOME="/tts_models"
ENTRYPOINT ["python3", "server.py"]