# NAOChat

This is a repo for performing natural language conversations via ChatGPT through a NAO robot using an external computer and micropohone.

## Setup

Create a new python virtual environemnt using python >= 3.8 and install the requirements. This can be done via the following terminal commands:
```
windows > py -3.11 -m venv env
windows > .\env\Scripts\activate
windows > pip install -r requirements.txt

linux > python3 -m venv env
linux > source env/bin/activate
linux > pip install -r requirement.txt
```

To later exit the python environment, use the terminal command `deactivate`. 

Go to https://platform.openai.com/account/api-keys and create a new API key. Save this key in a new file called `openai.key`.

If you intend to listen to the audio through your computer, you also need to install FFmpeg. See how on [their webpage](https://ffmpeg.org).

### NAO Setup

If you're intending to use this with a NAO a linux system is required. 

First, if not already pre-installed [install Python2](https://docs.python-guide.org/starting/install/linux/). Then three directories have to be collected.

Download [`nao-demo`](https://gitlab.liu.se/frelo91/nao-demo). Place it in this folder.
```
> git clone https://gitlab.liu.se/frelo91/nao-demo
```

Download [Choregrapher](https://community-static.aldebaran.com/resources/2.1.4.13/choregraphe/choregraphe-suite-2.1.4.13-linux64.tar.gz), uncompress the files and rename the directory `choregrapher`. Place it in this directory.
```
linux > wget https://community-static.aldebaran.com/resources/2.1.4.13/choregraphe/choregraphe-suite-2.1.4.13-linux64.tar.gz
linux > tar -xf choregraphe-suite-2.1.4.13-linux64.tar.gz
linux > mv choregraphe-suite-2.1.4.13-linux64 choregrapher
linux > rm choregraphe-suite-2.1.4.13-linux64.tar.gz
```
Download [PyNaoQI](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux32.tar.gz), uncompress the files and rename the directory `pynaoqi`. Place it in this directory.
```
linux > wget https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux32.tar.gz
linux > tar -xf pynaoqi-python2.7-2.1.4.13-linux32.tar.gz
linux > mv pynaoqi-python2.7-2.1.4.13-linux32 pynaoqi
linux > rm pynaoqi-python2.7-2.1.4.13-linux32.tar.gz
```
## Quickstart

### Chat Demo
To try chatting with the system, simply run `Chatter.py`. This demos both the streaming and full version.
```
> python Chatter.py
```

### Listener Demo
To try talking to the system, but with response in text form, run `Listener.py`.
```
> python Listener.py
```

### Talker Demo
To try talking to the system with responses in audio, though not through a NAO, run `Talker.py`. This requires [FFmpeg](https://ffmpeg.org) to be installed.

```
> python Talker.py
```

### NAOTalker Demo
To talk to ChatGPT via external microphone and get responses through NAO, run `NAOTalker.py`. Note that this requires a linux system and that you follow the steps in [NAO Setup](#nao-setup).
```
linux > python Talker.py
```