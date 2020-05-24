/** Sound player **/

const playSound = require('play-sound')

class SOUND {
  constructor (config) {
    this.config = config
  }

  init () {
    let opts = {
      "player": this.config.playProgram
    }
    this.player = playSound(opts)
    console.log("[MMM-Azure-TTS:SOUND] Program '" + this.config.playProgram + "' started and initialized.")
  }

  play (filename, successHandler, errorHandler) {
    if (!filename) {
      console.error("Input file null or empty!")
      return
    }
    var opt = {}
    var options = null
    var program = this.config.playProgram

    if (program == "cvlc") {
      options = "--play-and-exit"
      opt[program] = [options]
    }
    console.log("[MMM-Azure-TTS:SOUND] Audio starts playing file " + filename + " with program "  + program + " " + (options ? options : ""))

    this.player.play(filename, opt, (err) => {
      if (err) {
        console.error("[MMM-Azure-TTS:SOUND] Error occured during playing file " + filename)
        if(errorHandler)
          errorHandler(err)
      } else {
        console.log("[MMM-Azure-TTS:SOUND] Playing audio finished.")
        if(successHandler)
          successHandler("Playing audio finished.")
      }
    })
  }
}

module.exports = SOUND
