//
//  AppDelegate.m
//  Firestore_Example_macOS_objc
//
//  Created by Mathieu Tozer on 9/6/18.
//  Copyright © 2018 Google. All rights reserved.
//

#import "AppDelegate.h"
@import FirebaseCore;
@import FirebaseFirestore;

@interface AppDelegate ()

@property (weak) IBOutlet NSWindow *window;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
  // Insert code here to initialize your application
  [FIRApp configure];
  FIRCollectionReference *cals = [[FIRFirestore firestore] collectionWithPath:@"calendars"];
  NSLog(@"cals %@", cals);
}


- (void)applicationWillTerminate:(NSNotification *)aNotification {
  // Insert code here to tear down your application
}


@end
