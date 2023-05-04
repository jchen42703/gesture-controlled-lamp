//
//  GesturePicker.swift
//  Lampi
//
//  Created by Joseph Chen on 5/4/23.
//

import Foundation
import SwiftUI

class GestureController: UIViewController {
  private let gesturePickerView: UIPickerView = {
    let pickerView = UIPickerView()
    pickerView.translatesAutoresizingMaskIntoConstraints = false
    return pickerView
  }()

  private let gestureLabel: UILabel = {
    let label = UILabel()
    label.translatesAutoresizingMaskIntoConstraints = false
    return label
  }()
}
