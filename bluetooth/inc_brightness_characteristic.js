var util = require("util");
var events = require("events");
var bleno = require("bleno");
const yaml = require('js-yaml');
const fs = require("fs")

var CHARACTERISTIC_NAME = "Increase Brightness Gesture";

const currConfig = yaml.load(fs.readFileSync('../config.yaml', 'utf8'));
console.log(currConfig);

var IncreaseBrightnessCharacteristic = function (gestureState) {
  bleno.Characteristic.call(this, {
    uuid: "de9e20ae-f521-4cc3-9cc8-51ce9e7730f4",
    properties: ["read", "write"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: CHARACTERISTIC_NAME,
      }),
      new bleno.Descriptor({
        uuid: "2904",
        value: "Set increase",
      }),
    ],
  });

  this.deviceState = gestureState;
};

util.inherits(IncreaseBrightnessCharacteristic, bleno.Characteristic);

IncreaseBrightnessCharacteristic.prototype.onReadRequest = function (
  offset,
  callback
) {
  console.log("increase onReadRequest");
  if (offset) {
    callback(this.RESULT_ATTR_NOT_LONG, null);
  } else {
    // Read the yaml and return
    const currConfig = yaml.load(fs.readFileSync('../config.yaml', 'utf8'));
    const gesture = currConfig.increase_brightness_gesture
    console.log("increase brightness gesture: ", gesture)
    var data = Buffer.from(gesture);
    // data.writeUInt8(this.deviceState.value);
    // console.log("onReadRequest returning ", data);
    callback(this.RESULT_SUCCESS, data);
  }
};

IncreaseBrightnessCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  console.log("increase onWriteRequest");
  if (offset) {
    console.log("onWriteRequest RESULT_ATTR_NOT_LONG");
    callback(this.RESULT_ATTR_NOT_LONG);
  } else {
    var new_gesture = data.toString("utf-8");
    console.log("increase onWriteRequest ", new_gesture);
    // TODO: write to config
    currConfig.increase_brightness_gesture = new_gesture
    console.log("writing cfg: ", currConfig);
    const new_yaml = yaml.dump(currConfig, {
      'styles': {
        '!!null': 'canonical' // dump null as ~
      },
      'sortKeys': true        // sort object keys
    });
    fs.writeFileSync('../config.yaml', new_yaml);
    callback(this.RESULT_SUCCESS);
  }
};

module.exports = IncreaseBrightnessCharacteristic;
