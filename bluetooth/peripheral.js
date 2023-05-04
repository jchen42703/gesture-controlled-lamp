var child_process = require("child_process");
var device_id = child_process
  .execSync("cat /sys/class/net/eth0/address | sed s/://g")
  .toString()
  .replace(/\n$/, "");

process.env["BLENO_DEVICE_NAME"] = "GESTURE_LAMPI_" + device_id;
console.log("DEVICE: ", process.env["BLENO_DEVICE_NAME"])
var bleno = require("bleno");

var DeviceInfoService = require("./device-info-service");

const GestureState = require("./gesture_state")
var GestureService = require("./gesture_service");

const gestureState = new GestureState();
var deviceInfoService = new DeviceInfoService("CWRU", "LAMPI", "123456");
var gestureService = new GestureService(gestureState);

bleno.on("stateChange", function (state) {
  if (state === "poweredOn") {
    bleno.startAdvertising(
      "Gesture Lamp Config",
      [gestureService.uuid, deviceInfoService.uuid],
      function (err) {
        if (err) {
          console.log(err);
        }
      }
    );
  } else {
    bleno.stopAdvertising();
    console.log("not poweredOn");
  }
});

bleno.on("advertisingStart", function (err) {
  if (!err) {
    console.log("advertising...");
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([gestureService, deviceInfoService]);
    console.log("set services!")
  }
});
