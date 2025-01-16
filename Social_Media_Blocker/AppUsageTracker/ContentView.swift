import SwiftUI
import UserNotifications

struct ContentView: View {
    @State private var selectedApps: Set<String> = []
    @State private var timeLimit: Double = 60 // Default 60 minutes
    @State private var blockDuration: Double = 120 // Default 120 minutes
    
    let availableApps = ["Instagram", "Facebook", "Twitter", "TikTok"]
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Select Apps to Monitor")) {
                    ForEach(availableApps, id: \.self) { app in
                        Toggle(app, isOn: Binding(
                            get: { selectedApps.contains(app) },
                            set: { isSelected in
                                if isSelected {
                                    selectedApps.insert(app)
                                } else {
                                    selectedApps.remove(app)
                                }
                            }
                        ))
                    }
                }
                
                Section(header: Text("Time Settings")) {
                    Stepper("Time Limit: \(Int(timeLimit)) minutes", value: $timeLimit, in: 1...240)
                    Stepper("Block Duration: \(Int(blockDuration)) minutes", value: $blockDuration, in: 1...480)
                }
                
                Section {
                    Button("Start Monitoring") {
                        startMonitoring()
                    }
                }
            }
            .navigationTitle("Usage Monitor")
        }
    }
    
    func startMonitoring() {
        // Request notification permissions
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { success, error in
            if success {
                print("Notification permission granted")
            } else if let error = error {
                print(error.localizedDescription)
            }
        }
    }
} 