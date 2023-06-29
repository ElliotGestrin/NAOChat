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
Download [PyNaoQI](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux64.tar.gz), uncompress the files and rename the directory `pynaoqi`. Place it in this directory.
```
linux > wget https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
linux > tar -xf pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
linux > mv pynaoqi-python2.7-2.1.4.13-linux64 pynaoqi
linux > rm pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
```
## Quickstart

`main.py` implements a flexible system of premade configs. For further details on how to make your own, see [configs/README.md](./configs/README.md).

You can test the default via simply running `main.py`. This will let you talk to ChatGPT in the terminal.

```
> python main.py
```

You can also swap config via setting the config parameter when calling. The following will give you an instance that only greets you, and only when you greet it first.
```
> python main.py config=greeter
```

Each config file consists of parameters. You can change these during the call to `main.py`. This changes the mood and name of the default assistant.
```
> python main.py config=default name=Bob mood='southern and cheerfull'
``` 

Three notworthy parameters you can set for any config are: 
- `talker=speaker` to use your computers speaker, 
- `listener=mic` to use your computers microphone or 
- `talker=NAO` and `ip=123.456.789` (replaced with your NAO-IP) to talk from a NAO robot.
