//
//  LampiView.swift
//  Lampi
//

import SwiftUI

enum SupportedGestures: String {
  case MoveHandIn
  case MoveHandAway
  case DoNothing
}

struct LampiView: View {
    @ObservedObject var lamp: Lampi
    
    @Environment(\.presentationMode) var mode: Binding<PresentationMode>
    
    var gestures = [
        "Move hand in",
        "Move hand away",
        "Do nothing",
    ]
    @State private var increaseBrightnessIdx = 0
    @State private var decreaseBrightnessIdx = 1
    var body: some View {
        NavigationView {
            VStack(alignment: .leading) {
                Text("Current Operation to Gesture Configuration").font(.headline)
                HStack {
                    Text(verbatim: "Increase brightness ")
                    Picker(selection: $increaseBrightnessIdx, label: Text("Gesture")) {
                        ForEach(0 ..< gestures.count) {
                            Text(self.gestures[$0])
                        }
                    }
                }
                HStack {
                    Text(verbatim: "Decrease brightness")
                    Picker(selection: $decreaseBrightnessIdx, label: Text("Gesture")) {
                        ForEach(0 ..< gestures.count) {
                            Text(self.gestures[$0])
                        }
                    }
                }
            }.padding(.horizontal, 16)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        LampiView(lamp: Lampi(name: "LAMPI b827ebccda1f"))
            .previewDevice("iPhone 12 Pro")
            .previewLayout(.device)
    }
}
