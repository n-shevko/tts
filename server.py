from flask import Flask, request, send_file

from TTS.api import TTS
import torch
import io


device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
app = Flask(__name__)


@app.route("/speak", methods=["POST"])
def speak():
    wavs = tts.synthesizer.tts(request.json['text'], speaker_name='Sofia Hellen', language_name='en')
    out = io.BytesIO()
    tts.synthesizer.save_wav(wavs, out)
    return send_file(out, mimetype="audio/wav")


def main():
    app.run(host="::", port=5002)


if __name__ == "__main__":
    main()