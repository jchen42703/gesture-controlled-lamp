var util = require("util");
var bleno = require("bleno");

var IncreaseBrightnessCharacteristic = require("./inc_brightness_characteristic");
var DecreaseBrightnessCharacteristic = require("./dec_brightness_characteristic");

function GestureService(gestureState) {
  bleno.PrimaryService.call(this, {
    uuid: "E16D893B-5594-4940-B49C-CCE40F5ADA6A",
    characteristics: [new IncreaseBrightnessCharacteristic(gestureState),
                      new DecreaseBrightnessCharacteristic(gestureState)
                    ],
  });
}

util.inherits(GestureService, bleno.PrimaryService);

module.exports = GestureService;
