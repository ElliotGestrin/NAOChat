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

## Quickstart

### Chat Demo
To try chatting with the system, simply run `Chatter.py`. This demos both the streaming and full version.
```
> python Chatter.py
```