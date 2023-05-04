//
//  LampiApp.swift
//  Lampi
//

import SwiftUI
import Mixpanel

@main
struct LampiApp: App {
    #warning("Update DEVICE_NAME")
    let DEVICE_NAME = "GESTURE_LAMPI_b827eb1e9033"
    let USE_BROWSER = false

    var body: some Scene {
        WindowGroup {
            LampiView(lamp: Lampi(name: DEVICE_NAME))
        }
    }
}

