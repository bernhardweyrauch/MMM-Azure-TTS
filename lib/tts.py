#!/usr/bin/python
# coding: utf8
"""
MMM-Azure-TTS - MagicMirror Module
Text-To-Speech python implementation using Microsoft Azure Cloud Cognitive Services

By Bernhard Weyrauch - https://github.com/bernhardweyrauch/MMM-Azure-TTS
MIT Licensed.
"""

import glob, sys, signal, os, time
import os.path
from config import MMConfig
from azure_tts import TextToSpeech

# Ready config file
subscriptionKey = MMConfig.getSubscriptionKey()
tokenUrl = MMConfig.getTokenUrl()
baseUrl = MMConfig.getBaseUrl()
language = MMConfig.getLanguage()
person = MMConfig.getPerson()
timestr = time.strftime("%Y%m%d_%H%M%S")
targetFile = MMConfig.getTempDir() + "/" + timestr + "_TTS.wav"

# Start TTS logic
startTS = long(time.time()*1000)
inputText = sys.argv[2] # Ready from args
MMConfig.toNode("status", "Processing Text-To-Speech with input text: '" + inputText + "'")

app = TextToSpeech(subscriptionKey, tokenUrl, baseUrl, language, person, inputText, targetFile)
app.get_token() # Retrieve Azure Auth token
app.save_audio() # Process TTS and save audio file

if os.path.exists(targetFile) and os.path.getsize(targetFile) > 0:
    MMConfig.toNode("play", targetFile)
else:
    MMConfig.toNode("status", "Error: File " + targetFile + " does not exist or is empty!")

durationInMs = long(time.time()*1000)-startTS
MMConfig.toNode("status", "Text-To-Speech processing took " + str(durationInMs) + "ms.")
