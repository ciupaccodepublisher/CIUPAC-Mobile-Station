#ifndef UTILS_HPP
  #define UTILS_HPP
  #include <Arduino.h>
  #include "BluetoothSerial.h"
  #define GPS_UPDATE_IVAL_S 3
  
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  enum TimeSettingStatus{
  TS_NOT_SET,
  TS_WAITING_FOR_SECONDS,
  // TS_WAITING_FOR_TIMEZONE,
  TS_SET
  };
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  //------------------------------------------------------------------------------------------------
  void processReceivedStr(String& recvdStr);
  bool isItTimeNow();
  void waitForUserInput();
  // void printSpecialString(String& aStringM);
  void printSpecialCString(char* aStringM, bool hexM, bool oneMoreM);
  void assembleDataCStr(char* aCStringM,float temperatureM,float humidityM);
  void overwriteSpecialCString(char* aCStringM, uint8_t lengthM);
#endif