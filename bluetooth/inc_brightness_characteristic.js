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
    uuid: "7a4b0001-999f-4717-b63a-066e06971f59",
    properties: ["read", "write"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: CHARACTERISTIC_NAME,
      }),
      new bleno.Descriptor({
        uuid: "2904",
        value: Buffer.from("Set inc brightness gesture"),
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
  console.log("onReadRequest");
  if (offset) {
    callback(this.RESULT_ATTR_NOT_LONG, null);
  } else {
    // Read the yaml and return
    const currConfig = yaml.load(fs.readFileSync('../config.yaml', 'utf8'));
    const gesture = currConfig.increase_brightness_gesture
    console.log("gesture: ", gesture)
    var data = Buffer.from(gesture);
    // data.writeUInt8(this.deviceState.value);
    console.log("onReadRequest returning ", data);
    callback(this.RESULT_SUCCESS, data);
  }
};

IncreaseBrightnessCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  console.log("onWriteRequest");
  if (offset) {
    console.log("onWriteRequest RESULT_ATTR_NOT_LONG");
    callback(this.RESULT_ATTR_NOT_LONG);
  } else {
    var new_value = data.toString("utf-8");
    console.log("onWriteRequest ", new_value);
    // TODO: write to config
    callback(this.RESULT_SUCCESS);
  }
};

module.exports = IncreaseBrightnessCharacteristic;
