//
//  ContentView.swift
//  TONY_IOS
//
//  Created by João Lopes on 07/04/2022.
//

import SwiftUI
import Network
import MobileCoreServices

struct ContentView: View {
    
    @State private var showingAlert = false
    @State private var strrcv = ""
    @State private var encomendas = [
        "Fruit": "ba721314-b4b8-11ec-ad41-acde48001122",
        "Vodka": "ba683fec-b4b8-11ec-ad41-acde48001122",
        "Whiskey": "ba6ddf56-b4b8-11ec-ad41-acde48001122",
        "Pizza":"ba6f4346-b4b8-11ec-ad41-acde48001122",
        "Arduino Components": "ba70a89e-b4b8-11ec-ad41-acde48001122",
        "Donut":"ba74fc46-b4b8-11ec-ad41-acde48001122"
    ] //Encomendas
    
    var body: some View {
        VStack (spacing: 0) {
            GeometryReader { g in
                ScrollView {
                    Text("Encomendas")
                    List {
                        ForEach(self.encomendas.sorted(by: >), id: \.key) { key, value in
                            Text(key)
                                .onTapGesture {
                                    //ENVIA COMANDO
                                    connectToTcp(str: "FIND:" + value)
                                    showingAlert = true
                                    print("A")
                                }
                        }
                        .onDelete { index in
                            // delete item
                        }
                    }.frame(width: g.size.width - 5, height: g.size.height - 50, alignment: .center)
                    
                }
            }
            
            Button(action: {
                showingAlert = true
                connectToTcp(str: "VOICE_RECOGNITION")
            }) {
               // Some view, example below uses Image
               Image(systemName: "mic.fill")
            }.scaleEffect(3)
            //.alert(isPresented: $showingAlert) {
             //           Alert(title: Text(strrcv), message: Text("ALERTA"), dismissButton: .default(Text("OK")))
               //     }
        }
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
        
        func receivemsg(){
        connection.receiveMessage { (data, context, isComplete, error) in
            if (isComplete) {
                print("Receive is complete, count bytes: \(data!.count)")
                strrcv = String(bytes: data!, encoding: .utf8)!
                print(strrcv)
                if (data != nil) {
    //                    print(data!.byteToHex())
                } else {
                    print("Data == nil")
                }
            }
        }
        }
        
        //connection.cancel()
        }
}


    
        //
    //}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
