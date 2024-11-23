# Installation
```
git clone https://github.com/n-shevko/tts.git
cd tts
pip install -r packages
```

# Usage

You have to run 2 commands (on separate console tabs):
```
docker run --rm -it -p 5002:5002 --gpus all -v tts_models:/tts_models nikos123/tts:1.0.0
python client.py # only if you want Ctrl+C to work
```
if you don't have nvidia gpu then remove --gpus all.
Then go to http://127.0.0.1:5002/ where you can provide text from file or paste it into textarea.

# if you have NVIDIA gpu (may not help)

1. Install "NVIDIA Container Toolkit". Do steps 1-3 from section "Installing with Apt"
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt

2. Reload docker
sudo systemctl daemon-reload
sudo systemctl restart docker

Now when you select text and press Ctrl+C it will be spoken.


The first run of docker command will download model so it may take some time.
When you verbolize a medium/big amount of text then you have to wait 10+ seconds during which speech will be generated (you won't hear anything during generation).


