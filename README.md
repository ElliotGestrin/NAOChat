# NAOChat

This is a repo for performing natural language conversations via ChatGPT through a NAO robot using an external computer and micropohone.

## Setup

Create a new python virtual environemnt using python >= 3.10 and install the requirements. This can be done via the following terminal commands:
```
# Windows
py -3.11 -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```
```
# Linux
python3 -m venv env
source env/bin/activate
pip install -r requirement.txt
```

To later exit the python environment, use the terminal command `deactivate`. 

Go to https://platform.openai.com/account/api-keys and create a new API key. Save this key in a new file called `openai.key`.

If you intend to listen to the audio through yofur computer, you also need to install FFmpeg. See how on [their webpage](https://ffmpeg.org).

### NAO Setup

If you intend to use a NAO robot you need a Linux system and some further setup. Follow the [NAO specific instructions](src/NAO/README.md).

Note that this also comes with the option to manually control your NAO manually. See the [NAO specific instructions](src/NAO/README.md) for details.

## Quickstart

`main.py` implements a flexible system of premade configs. For further details on how to make your own, see [configs/README.md](./configs/README.md).

You can test the default via simply running `main.py`. This will let you talk to ChatGPT in the terminal.

```
python main.py
```

You can also swap config via setting the config parameter when calling. The following will give you an instance that only greets you, and only when you greet it first.
```
python main.py config=greeter
```

Each config file consists of parameters. You can change these during the call to `main.py`. This changes the mood and name of the default assistant.
```
python main.py config=default name=Bob mood='southern and cheerfull'
``` 

Three notworthy parameters you can set for any config are:
- `talker=speaker` to use your computers speakers.
- `listener=mic` to use your computers microphone. 
- `talker=NAO` and `ip=123.456.789` (replaced with your NAO-IP) to talk from a NAO robot. This requires the [NAO Setup](src/NAO/README.md).