# NAOChat

This is a repo for performing natural language conversations via ChatGPT through a NAO robot using an external computer and micropohone.

## Setup

Create a new python virtual environemnt using python >= 3.8 and install the requirements. On my windows system this is done via the following terminal commands:
```
> py -3.11 -m venv env
> .\env\Scripts\activate
> pip install -r requirements.txt
```

Go to https://platform.openai.com/account/api-keys and create a new API key. Save this key in a new file called `openai.key`.

If you intend to listen to the audio through your computer, you also need to install FFmpeg. See how on [their webpage](https://ffmpeg.org).

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