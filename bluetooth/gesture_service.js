var util = require("util");
var bleno = require("bleno");

var IncreaseBrightnessCharacteristic = require("./inc_brightness_characteristic");
var DecreaseBrightnessCharacteristic = require("./dec_brightness_characteristic");

function GestureService(gestureState) {
  bleno.PrimaryService.call(this, {
    uuid: "0001A7D3-D8A4-4FEA-8174-1736E808C066",
    characteristics: [new IncreaseBrightnessCharacteristic(gestureState),
                      new DecreaseBrightnessCharacteristic(gestureState)
                    ],
  });
}

util.inherits(GestureService, bleno.PrimaryService);

module.exports = GestureService;
