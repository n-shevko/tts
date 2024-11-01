import pyaudio
import wave
import io
import requests
import pyperclip
import time


def play_wav(audio_data):
    CHUNK = 1024
    with wave.open(audio_data, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        while len(data := wf.readframes(CHUNK)):
            stream.write(data)
        stream.close()
        p.terminate()


if __name__ == "__main__":
    previous_text = pyperclip.paste()
    print("Select text -> Ctrl+C -> The text will be spoken")
    while True:
        current_text = pyperclip.paste()
        if current_text != previous_text:
            previous_text = current_text
            response = requests.post(
                'http://127.0.0.1:5002/speak',
                json={'text': current_text}
            )
            audio_data = io.BytesIO(response.content)
            play_wav(audio_data)
        time.sleep(0.5)