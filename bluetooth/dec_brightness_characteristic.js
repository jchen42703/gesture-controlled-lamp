var util = require("util");
var events = require("events");
var bleno = require("bleno");
const yaml = require('js-yaml');
const fs = require("fs")

var CHARACTERISTIC_NAME = "Decrease Brightness Gest";

const currConfig = yaml.load(fs.readFileSync('../config.yaml', 'utf8'));
console.log(currConfig);

var DecreaseBrightnessCharacteristic = function (gestureState) {
  bleno.Characteristic.call(this, {
    uuid: "6a104faf-832b-4a66-9a6c-7a1cf924f223",
    properties: ["read", "write"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: CHARACTERISTIC_NAME,
      }),
      new bleno.Descriptor({
        uuid: "2904",
        value: "Set decrease",
      }),
    ],
  });

  this.deviceState = gestureState;
};

util.inherits(DecreaseBrightnessCharacteristic, bleno.Characteristic);

DecreaseBrightnessCharacteristic.prototype.onReadRequest = function (
  offset,
  callback
) {
  console.log("decrease brightness onReadRequest");
  if (offset) {
    callback(this.RESULT_ATTR_NOT_LONG, null);
  } else {
    // Read the yaml and return
    const currConfig = yaml.load(fs.readFileSync('../config.yaml', 'utf8'));
    const gesture = currConfig.decrease_brightness_gesture
    console.log("decrease brightness gesture: ", gesture)
    var data = Buffer.from(gesture);
    // data.writeUInt8(this.deviceState.value);
    // console.log("decrease onReadRequest returning ", data);
    callback(this.RESULT_SUCCESS, data);
  }
};

DecreaseBrightnessCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  console.log("decrease brightness onWriteRequest");
  if (offset) {
    console.log("onWriteRequest RESULT_ATTR_NOT_LONG");
    callback(this.RESULT_ATTR_NOT_LONG);
  } else {
    var new_gesture = data.toString("utf-8");
    console.log("decrease brightness onWriteRequest gest: ", new_gesture);
    // TODO: write to config
    currConfig.decrease_brightness_gesture = new_gesture
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

module.exports = DecreaseBrightnessCharacteristic;
