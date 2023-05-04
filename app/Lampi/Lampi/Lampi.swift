//
//  Lampi.swift
//  Lampi
//

import Foundation
import CoreBluetooth
import Combine
import SwiftUI

class Lampi: NSObject, ObservableObject {
    let name: String
    @Published var state = State() {
        didSet {
            if oldValue != state {
                updateDevice()
            }
        }
    }

    private func setupPeripheral() {
        if let lampiPeripheral = lampiPeripheral  {
            lampiPeripheral.delegate = self
        }
    }

    private var bluetoothManager: CBCentralManager?

    var lampiPeripheral: CBPeripheral? {
        didSet {
            setupPeripheral()
        }
    }
    
    private var incBrightnessChar: CBCharacteristic?
    private var decBrightnessChar: CBCharacteristic?

    // MARK: State Tracking
    private var skipNextDeviceUpdate = false
    private var pendingBluetoothUpdate = false

    init(name: String) {
        self.name = name
        super.init()

        self.bluetoothManager = CBCentralManager(delegate: self, queue: nil)
    }

    init(lampiPeripheral: CBPeripheral) {
        guard let peripheralName = lampiPeripheral.name else {
            fatalError("Lampi must initialized with a peripheral with a name")
        }

        self.lampiPeripheral = lampiPeripheral
        self.name = peripheralName

        super.init()

        self.setupPeripheral() // properties set in init() do not trigger didSet
    }
}

extension Lampi {
    static let SERVICE_UUID = CBUUID(string: "E16D893B-5594-4940-B49C-CCE40F5ADA6A")
    static let INC_BRIGHTNESS_UUID = CBUUID(string: "CC8E0047-61F3-487E-96A1-637A4450AE33")
    static let DEC_BRIGHTNESS_UUID = CBUUID(string: "13ACBAEB-4DB2-425E-B067-49A5472592D2")

    private var shouldSkipUpdateDevice: Bool {
        return skipNextDeviceUpdate || pendingBluetoothUpdate
    }

    private func updateDevice(force: Bool = false) {
        if state.isConnected && (force || !shouldSkipUpdateDevice) {
            pendingBluetoothUpdate = true
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
                self?.writeDecBrightnessGesture()
                self?.writeIncBrightnessGesture()

                self?.pendingBluetoothUpdate = false
            }
        }

        skipNextDeviceUpdate = false
    }
    
    private func writeIncBrightnessGesture() {
        if let incBrightnessChar = incBrightnessChar {
            let data = Data(bytes: Array(state.incBrightnessGesture.utf8), count: 1)
            lampiPeripheral?.writeValue(data, for: incBrightnessChar, type: .withResponse)
        }
    }
    
    private func writeDecBrightnessGesture() {
        if let decBrightnessChar = decBrightnessChar {
            let data = Data(bytes: Array(state.decBrightnessGesture.utf8), count: 1)
            lampiPeripheral?.writeValue(data, for: decBrightnessChar, type: .withResponse)
        }
    }
}

extension Lampi {
    struct State: Equatable {
        var isConnected = false
        var incBrightnessGesture = "Move hand in"
        var decBrightnessGesture = "Move hand away"
    }
}

extension Lampi: CBCentralManagerDelegate {
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if bluetoothManager?.state == .poweredOn {
            print("Scanning for Lampis")
            bluetoothManager?.scanForPeripherals(withServices: [Lampi.SERVICE_UUID])
        }
    }

    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        if peripheral.name == name {
            print("Found \(name)")

            lampiPeripheral = peripheral

            bluetoothManager?.stopScan()
            bluetoothManager?.connect(peripheral)
        }
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        print("Connected to peripheral \(peripheral)")
        peripheral.delegate = self
        peripheral.discoverServices([Lampi.SERVICE_UUID])
    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        print("Disconnected from peripheral \(peripheral)")
        state.isConnected = false
        bluetoothManager?.connect(peripheral)
    }
}

extension Lampi: CBPeripheralDelegate {
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else { return }

        for service in services {
            print("Found: \(service)")
            peripheral.discoverCharacteristics(nil, for: service)
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        guard let characteristics = service.characteristics else { return }

        for characteristic in characteristics {
            print("Char: ", characteristic.uuid)
            switch characteristic.uuid {
            case Lampi.DEC_BRIGHTNESS_UUID:
                self.decBrightnessChar = characteristic
                peripheral.readValue(for: characteristic)

            case Lampi.INC_BRIGHTNESS_UUID:
                self.incBrightnessChar = characteristic
                peripheral.readValue(for: characteristic)

            default:
                continue
            }
        }

        // not connected until all characteristics are discovered
        // if self.hsvCharacteristic != nil && self.brightnessCharacteristic != nil && self.onOffCharacteristic != nil {
         //   skipNextDeviceUpdate = true
            //state.isConnected = true
        //}
    }

    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        guard let updatedValue = characteristic.value,
              !updatedValue.isEmpty else { return }
        switch characteristic.uuid {
        case Lampi.INC_BRIGHTNESS_UUID:
            state.incBrightnessGesture = String(decoding: updatedValue, as: UTF8.self)
            print("Increase Brightness Gesture: ", state.incBrightnessGesture)

        case Lampi.DEC_BRIGHTNESS_UUID:
            state.decBrightnessGesture = String(decoding: updatedValue, as: UTF8.self)
        
        print("State: ", state)
        default:
            print("Unhandled Characteristic UUID: \(characteristic.uuid)")
        }
    }
}
