//
//  AppDelegate.swift
//  Firestore_Example_macOS
//
//  Created by Mathieu Tozer on 9/6/18.
//  Copyright © 2018 Google. All rights reserved.
//

import Cocoa
import FirebaseCore
import FirebaseFirestore

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {

  @IBOutlet weak var window: NSWindow!


  func applicationDidFinishLaunching(_ aNotification: Notification) {
    // Insert code here to initialize your application
    FirebaseApp.configure()
    
    let db = Firestore.firestore()
    db.collection("calendars").getDocuments() { (snapshot, err) in
      if let err = err {
        print(err)
      } else {
        for doc in snapshot!.documents {
          print(doc.data())
        }
      }
    }
  }

  func applicationWillTerminate(_ aNotification: Notification) {
    // Insert code here to tear down your application
  }


}

