var events = require('events');
var util = require('util');
var mqtt = require('mqtt');

function GestureMappingState() {
    events.EventEmitter.call(this);

    this.inc_brightness_gesture = "Move hand away";
    this.dec_brightness_gesture = "Move hand in";
}

util.inherits(GestureMappingState, events.EventEmitter);

GestureMappingState.prototype.set_inc_brightness_gesture = function(new_gesture) {
    this.inc_brightness_gesture = new_gesture;
    console.log(`New gesture: ${new_gesture}`)
};

GestureMappingState.prototype.set_dec_brightness_gesture = function(new_gesture) {
    this.dec_brightness_gesture = new_gesture;
    console.log(`New gesture: ${new_gesture}`)
};

module.exports = GestureMappingState;
