"""
Script for NAO Robot Text-to-Speech - Python 2.7.18

Author: [Johan Holtz, Mathias Ahlgren]
Date: [2023-05-18]

Usage:

Call as a subprocess and provide Text as an argument, Naoqi Sdk must exist

Possible Problems:

    -  Opening a new ALTextToSpeech for each communication --> needs to be tested
"""

import sys
import time
import naoqi

# NAO robot IP address and port number
NAO_IP = "nao_robot_ip"
NAO_PORT = 9559

# Retrieve the text to be spoken from command-line argument
text = sys.argv[1]

# Get the current time
current = time.time()

# Create an instance of ALTextToSpeech proxy for NAO robot
tts_proxy = naoqi.ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)

# Set the desired language for text-to-speech
tts_proxy.setLanguage("English")

# Set the desired voice for text-to-speech
tts_proxy.setVoice("naoenu")

# Use text-to-speech to speak the provided text
tts_proxy.say(text)

print("Elapsed time:", time.time() - current)