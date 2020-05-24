'use strict';
const NodeHelper = require('node_helper');
const PythonShell = require('python-shell');
const Sound = require("./lib/sound.js")

module.exports = NodeHelper.create({

  executeTTS: function (inputText) {
    const self = this;
    const ttsExecutable = 'modules/' + this.name + '/lib/tts.py';
    const args = [JSON.stringify(this.config), inputText];
    //console.info("Execute " + ttsExecutable + " with args: " + inputText);
    const pyshell = new PythonShell(ttsExecutable, { mode: 'json', args: args });
    pyshell.on('message', function (message) {
      if (message.hasOwnProperty('status')) {
        console.log("[" + self.name + "] " + message.status);
      } else if (message.hasOwnProperty('play')) {
        var filename = message.play
        console.log("[" + self.name + "] Play file " + filename);
        var success = function(message) {
          if(self.config.deleteFile) {
            // delete file
            var fs = require('fs');
            fs.unlink(filename, function(msg) {
              console.log("[" + self.name + "] File " + filename + " deleted.");
            });
          }
        }
        var error = function(error) {
          console.error("[" + self.name + "] Error during playing file " + filename);
        }
        self.sound.play(filename, success, error)
      }
    });
    pyshell.end(function (err) {
      if (err) {
        console.error("[" + self.name + "] TTS completed with error=", err);
        self.sendSocketNotification('Azure_TTS_Error', err);
      } else {
        console.log("[" + self.name + "] TTS completed.");
        self.sendSocketNotification('Azure_TTS_Done', "");
      }
    });
  },

  // Subclass socketNotificationReceived received.
  socketNotificationReceived: function(notification, payload) {
    if(notification === 'Azure_TTS_Config') {
      this.config = payload;
      // init sound
      this.sound = new Sound(this.config)
      this.sound.init()
      this.sendSocketNotification('Azure_TTS_Ready', "Azure TTS module is initialized and ready.");
    } else
    if(notification === 'Azure_TTS' && payload) {
      this.executeTTS(payload);
    }
  }
})
