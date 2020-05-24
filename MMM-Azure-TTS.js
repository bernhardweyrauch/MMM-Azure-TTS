/* global Module */

/* Magic Mirror
 * Module: MMM-Azure-TTS
 *
 * By Bernhard Weyrauch - https://github.com/bernhardweyrauch/MMM-Azure-TTS
 * MIT Licensed.
 */

Module.register("MMM-Azure-TTS", {

  defaults: {
    subscriptionKey : "REQUIRED__PLEASE_FILL_IN",
    tokenUrl: "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken",
    baseUrl: "https://westeuropa.tts.speech.microsoft.com/",
    // Support languages and persons see: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech
    language: "de", // de, en
    person: "de-DE-KatjaNeural",
    tmpDir: "/var/ramdrive",  // to store the temporary *.wav file
    playProgram: "aplay", // program to play the *.wav file. Optional include parameter -d N where N is the audio card
    deleteFile: true  // should the generated audio file deleted after playing it
  },

  start: function() {
    Log.info("Starting module: " + this.name);
    this.sendSocketNotification("Azure_TTS_Config", this.config);
  },

  getDom: function () {
    return "";
  },

  getStyles: function() {
    return [];
  },

  notificationReceived: function(notification, payload, sender) {
    if (notification === "Azure_TTS" && typeof payload === "string" && payload.length > 0) {
      Log.info(this.name + " received notification to TTS text '" + payload + "'.");
      this.sendSocketNotification("Azure_TTS", payload);
    }
  },

  socketNotificationReceived: function(notification, payload) {
    if (notification === "Azure_TTS_Ready") {
      Log.info(this.name + " is ready. Message=", payload);
    } else if (notification === "Azure_TTS_Done") {
      Log.info(this.name + " completed.");
    } else if (notification === "Azure_TTS_Error") {
      Log.eerror(this.name + " completed with error ", payload);
    }
  }

});
