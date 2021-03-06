/*
 * Copyright 2017 Google
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#import <FirebaseFirestore/FIRCollectionReference.h>

#import <XCTest/XCTest.h>

#import "Firestore/Example/Tests/API/FSTAPIHelpers.h"

NS_ASSUME_NONNULL_BEGIN

@interface FIRCollectionReferenceTests : XCTestCase
@end

@implementation FIRCollectionReferenceTests

- (void)testEquals {
  FIRCollectionReference *referenceFoo = FSTTestCollectionRef("foo");
  FIRCollectionReference *referenceFooDup = FSTTestCollectionRef("foo");
  FIRCollectionReference *referenceBar = FSTTestCollectionRef("bar");
  XCTAssertEqualObjects(referenceFoo, referenceFooDup);
  XCTAssertNotEqualObjects(referenceFoo, referenceBar);

  XCTAssertEqual([referenceFoo hash], [referenceFooDup hash]);
  XCTAssertNotEqual([referenceFoo hash], [referenceBar hash]);
}

@end

NS_ASSUME_NONNULL_END
