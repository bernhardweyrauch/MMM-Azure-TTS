#!/usr/bin/python
# coding: utf8
"""
MMM-Azure-TTS - MagicMirror Module
Text-To-Speech python implementation using Microsoft Azure Cloud Cognitive Services
Configuration object file

By Bernhard Weyrauch - https://github.com/bernhardweyrauch/MMM-Azure-TTS
MIT Licensed.
"""
import os
import json
import sys
import platform

class MMConfig ():
    CONFIG_DATA = json.loads(sys.argv[1]);  # config JSON
    SUBSCRIPTION_KEY = 'subscriptionKey'
    TOKEN_URL = 'tokenUrl'
    AZURE_BASE_URL = 'baseUrl'
    LANGUAGE = 'language'
    PERSON = 'person'
    TMP_FOLDER = 'tmpDir'

    @classmethod
    def toNode(cls, type, message):
        print(json.dumps({type: message}))
    @classmethod
    def getSubscriptionKey(cls):
        return cls.get(cls.SUBSCRIPTION_KEY)
    @classmethod
    def getTokenUrl(cls):
        return cls.get(cls.TOKEN_URL)
    @classmethod
    def getBaseUrl(cls):
        return cls.get(cls.AZURE_BASE_URL)
    @classmethod
    def getLanguage(cls):
        return cls.get(cls.LANGUAGE)
    @classmethod
    def getPerson(cls):
        return cls.get(cls.PERSON)
    @classmethod
    def getTempDir(cls):
        return cls.get(cls.TMP_FOLDER)

    @classmethod
    def get(cls,key):
        return cls.CONFIG_DATA[key]
