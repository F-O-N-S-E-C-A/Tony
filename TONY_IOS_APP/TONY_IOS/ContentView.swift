//
//  ContentView.swift
//  TONY_IOS2
//
//  Created by João Lopes on 08/04/2022.
//

import SwiftUI
import Network

struct ContentView: View {
    @State private var encomendas = [
        "Fruit": "ba721314-b4b8-11ec-ad41-acde48001122",
        "Vodka": "ba683fec-b4b8-11ec-ad41-acde48001122",
        "Whiskey": "ba6ddf56-b4b8-11ec-ad41-acde48001122",
        "Pizza":"ba6f4346-b4b8-11ec-ad41-acde48001122",
        "Arduino Components": "ba70a89e-b4b8-11ec-ad41-acde48001122",
        "Donut":"ba74fc46-b4b8-11ec-ad41-acde48001122"
    ] //Encomendas
    
    var body: some View {
        VStack {
            ScrollView {
                VStack (spacing: 75){
                    ForEach(self.encomendas.sorted(by: >), id: \.key) { key, value in
                        HStack {
                            Text(key)
                            
                            Spacer()
                            
                            Button(action: {
                                connectToTcp(str: "FIND:" + value)
                            }) {
                               // Some view, example below uses Image
                               Image(systemName: "bag.fill")
                            }.scaleEffect(3)
                        }
                    }
                    .onDelete { index in
                        // delete item
                    }
            }.padding(50)
            
        }
            
            Spacer()
            
            Button(action: {
                connectToTcp(str: "VOICE_RECOGNITION")
            }) {
               // Some view, example below uses Image
               Image(systemName: "mic.fill")
                    .foregroundColor(.white)
            }.scaleEffect(3)
                .padding(70)
        }
        .preferredColorScheme(.dark)
    }
    
    func connectToTcp(str: String) {
            let PORT: NWEndpoint.Port = 1999
            let  ipAddress :NWEndpoint.Host = "192.168.4.3" //QUAL O TEU IP?
            let queue = DispatchQueue(label: "TCP Client Queue")
            
            let tcp = NWProtocolTCP.Options.init()
            tcp.noDelay = true
            let params = NWParameters.init(tls: nil, tcp: tcp)
            let connection = NWConnection(to: NWEndpoint.hostPort(host: ipAddress, port: PORT), using: params)
            
            connection.stateUpdateHandler = { (newState) in

                switch (newState) {
                case .ready:
                    print("Socket State: Ready")
                    UserDefaults.standard.set(true, forKey: "isConnected")
                    print("Sending")
                    sendMSG(message: str)
                    //receivemsg()
                    
                    //receive()
                default:
                    UserDefaults.standard.set(false, forKey: "isConnected")

                    break
                }
            }
            connection.start(queue: queue)
        
        func sendMSG(message: String) {
                let message1 = message
                let content: Data = message1.data(using: .utf8)!
                connection.send(content: content, completion: NWConnection.SendCompletion.contentProcessed(({ (NWError) in
                    if (NWError == nil) {
                        print("Data was sent to TCP destination ")
                        connection.cancel()
                        
                    } else {
                        print("ERROR! Error when data (Type: Data) sending. NWError: \n \(NWError!)")
                    }
                })))
            }
        //connection.cancel()
        }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
