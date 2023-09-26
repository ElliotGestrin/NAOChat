# NAO 
## Setup
If you're intending to use this with a NAO a linux system is required. 

First, if not already pre-installed [install Python2](https://docs.python-guide.org/starting/install/linux/). Then three directories have to be collected.

Download [Choregrapher](https://community-static.aldebaran.com/resources/2.1.4.13/choregraphe/choregraphe-suite-2.1.4.13-linux64.tar.gz), uncompress the files and rename the directory `choregrapher`. Place it in this directory.
```
# Linux only
wget https://community-static.aldebaran.com/resources/2.1.4.13/choregraphe/choregraphe-suite-2.1.4.13-linux64.tar.gz
tar -xf choregraphe-suite-2.1.4.13-linux64.tar.gz
mv choregraphe-suite-2.1.4.13-linux64 choregrapher
rm choregraphe-suite-2.1.4.13-linux64.tar.gz
```
Download [PyNaoQI](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux64.tar.gz), uncompress the files and rename the directory `pynaoqi`. Place it in this directory.
```
# Linux only
wget https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
tar -xf pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
mv pynaoqi-python2.7-2.1.4.13-linux64 pynaoqi
rm pynaoqi-python2.7-2.1.4.13-linux64.tar.gz
```
## Usage
The NAO can be used in two ways. Via ChatGPT or as a manual puppet.

### ChatGPT
To use the NAO with ChatGPT simply run the regular `main.py` as described in the [main readme](../../README.md), but adding the `talker=nao` and `ip=123.456.789`, replaced with your NAOs IP, parameters.

```
# From the repository root
python main.py talker=nao ip=123.456.789
```

### Puppeting
You can manually puppet the NAO. This is based on Fredrik Löfgrens [nao-demo](https://gitlab.liu.se/frelo91/nao-demo) repo, though has been somewhat reworked by me. 

To do this, you need to source `py2_nao_source.sh` and then run `NAOTalkerPy2.py` with python2. Note that `py2_nao_source.sh` is automatically created the first time you run the regular [ChatGPT](#chatgpt) mode, so if the file isn't there run it first. 

```
# From this folder
source py2_nao_source.sh
python2 NAOTalkerPy2.py 123.456.789 Language Volume
```
This will open an interactive terminal. Here you can write specific commands, such as "stand" or sentences which will be spoken. As some of the commands use behaviours pre-installed on the NAO these might not work for you.

Note that this sourcing process might cause further attempts at using python3 for regular GPT-behaviour to fail due to segmentation fault. If so, simply use a new terminal for this. 