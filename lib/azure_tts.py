#!/usr/bin/python
# coding: utf8
#
# https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python-text-to-speech

import os, requests, time
from xml.etree import ElementTree

class TextToSpeech(object):
    def __init__(self, subscription_key, tokenUrl, baseUrl, language, person, textInput, targetFile):
        self.subscription_key = subscription_key
        self.token_url = tokenUrl
        self.base_url = baseUrl
        self.language = language
        self.person = person
        self.tts = textInput
        self.targetFile = targetFile
        self.access_token = None

    def get_body_language(self, language):
        if language == "de":
            return "de-de"
        elif language == "en":
            return "en-us"

    def get_voice_language(self, language):
        if language == "de":
            return "de-US"
        elif language == "en":
            return "en-US"

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(self.token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        endpoint_url = self.base_url + '/cognitiveservices/v1'
        bodyLang = self.get_body_language(self.language)
        voiceLang = self.get_voice_language(self.language)
        # https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'MagicMirror-Client'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', bodyLang)
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', voiceLang)
        voice.set('name', self.person)
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)
        response = requests.post(endpoint_url, headers=headers, data=body)

        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open(self.targetFile, 'wb') as audio:
                audio.write(response.content)
                #print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        #else:
        #    print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        #    print("Reason: " + str(response.reason) + "\n")

    def get_voices_list(self):
        endpoint_url = self.base_url + '/cognitiveservices/voices/list'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(endpoint_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
