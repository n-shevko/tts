import os
import json

from pydub import AudioSegment
from flask import Flask, request, send_file, render_template, jsonify

from TTS.api import TTS
import torch
import io


if os.path.exists('/tts_models'):
    path = '/tts_models/data.json'
else:
    path = os.path.join(os.getcwd(), 'data.json')


def load_data():
    if not os.path.exists(path):
        return {}
    else:
        with open(path, 'r') as f:
            return json.loads(f.read())


def get(key, default=None):
    data = load_data()
    return data.get(key, default)


def update(key, value):
    data = load_data()
    data[key] = value
    with open(path, 'w') as f:
        f.write(json.dumps(data))


device = "cuda" if torch.cuda.is_available() else "cpu"
model = get("model", "tts_models/multilingual/multi-dataset/xtts_v2")
speaker = get('speaker', 'Sofia Hellen')
tts = TTS(model).to(device)
app = Flask(__name__)


def get_speakers():
    if not tts.is_multi_speaker:
        return []
    else:
        return list(tts.synthesizer.tts_model.speaker_manager.name_to_id)


@app.route("/", methods=["GET"])
def main():
    data = {
        'model': model,
        'models': tts.models,
        'source': 'file',
        'speaker': speaker,
        'speakers': get_speakers(),
        'speed': 1.0
    }
    data.update(load_data())
    return render_template('main.html', data=data)


@app.route("/switch_model", methods=["POST"])
def switch_model():
    global tts
    global model
    global speaker
    model = request.json['model']
    tts = TTS(model).to(device)
    speakers = get_speakers()
    if speakers:
        speaker = speakers[0]
    else:
        speaker = ''
    update('speaker', speaker)
    return jsonify({'speakers': speakers, 'speaker': speaker})


def generate_wav():
    kwargs = {
        'language_name': 'en',
        'speed': float(get('speed', 1.0)),
        'enable_text_splitting': True
    }
    speakers = get_speakers()
    if speaker and speakers:
        kwargs['speaker_name'] = speaker

    if 'file' in request.files:
        uploaded_file = request.files['file']
        text = uploaded_file.read().decode('utf-8')
    else:
        text = request.form['text']
    wavs = tts.synthesizer.tts(text, **kwargs)
    out = io.BytesIO()
    tts.synthesizer.save_wav(wavs, out)
    return out


@app.route("/create_mp3", methods=["POST"])
def create_mp3():
    mp3_file = io.BytesIO()
    AudioSegment.from_file(generate_wav(), format="wav").export(mp3_file, format='mp3')
    return send_file(mp3_file, mimetype="audio/mp3")


@app.route("/speak", methods=["POST"])
def speak():
    return send_file(generate_wav(), mimetype="audio/wav")


@app.route("/save_params", methods=["POST"])
def save_params():
    for k, v in request.json.items():
        update(k, v)
    return jsonify({})


def main():
    print(f"Used device: {device}")
    app.run(host="::", port=5002)


if __name__ == "__main__":
    main()