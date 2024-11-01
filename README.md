# Installation
```
git clone https://github.com/n-shevko/tts.git
cd tts
pip install -r packages
```

# Usage

You have to run 2 commands (on separate console tabs):
```
docker run --rm -it -p 5002:5002 -v tts_models:/tts_models nikos123/tts:1.0.0
python client.py
```

Now when you select text and press Ctrl+C it will be spoken.


The first run of docker command will download model so it may take some time.
When you verbolize a medium/big amount of text then you have to wait 10+ seconds during which speech will be generated (you won't hear anything during generation).


