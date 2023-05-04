#! /usr/bin/env node
var child_process = require("child_process");
var device_id = child_process
  .execSync("cat /sys/class/net/eth0/address | sed s/://g")
  .toString()
  .replace(/\n$/, "");

process.env["BLENO_DEVICE_NAME"] = "LAMPI " + device_id;

var serviceName = "LampiService";
var bleno = require("bleno");

var LampiState = require("./lampi-state");
var LampiService = require("./lampi-service");

var lampiState = new LampiState();
var lampiService = new LampiService(lampiState);
var deviceInfoService = new DeviceInfoService("CWRU", "LAMPI", device_id);

bleno.on("advertisingStart", function (err) {
  if (!err) {
    console.log("advertising...");
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([lampiService]);
  }
});

bleno.on("accept", function (clientAddress) {
  console.log("accept: " + clientAddress);
});

bleno.on("disconnect", function (clientAddress) {
  console.log("disconnect: " + clientAddress);
});
