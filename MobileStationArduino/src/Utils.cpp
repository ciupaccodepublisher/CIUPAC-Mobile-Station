#include "Utils.hpp"

BluetoothSerial serialBT;
TimeSettingStatus timeSStatus;
timeval aTimePckt;
time_t previousTimestamp=0;
//------------------------------------------------------------------------------------------------
/*
BTWrapper::BTWrapper(BluetoothSerial * serialBTPM)
{
  serialBTP= serialBTPM;
}
*/
//------------------------------------------------------------------------------------------------
// void BTWrapper::processReceivedStr(String& recvdStr){
void processReceivedStr(String& recvdStr){
  // DAD
  Serial.print(F("<-: "));
  Serial.println(recvdStr);

// INFO: Returns 0 when true
  int strCoincidence= recvdStr.compareTo("PING");
  // Ping
  if (strCoincidence==0){
    serialBT.print("KA");
    Serial.print(F("->: "));
    Serial.println("KA");
  }
  else{
    // No ping
    strCoincidence= recvdStr.compareTo("SETTIME");
    // SETTIME command, wait for new packet
    if (strCoincidence==0){
      timeSStatus= TS_WAITING_FOR_SECONDS;
    }
    // Time set continuation
    else {
      // if (timeSStatus=TS_WAITING_FOR_SECONDS){
          aTimePckt.tv_sec= recvdStr.toInt();
          aTimePckt.tv_usec= 0;
          // timeSStatus= TS_WAITING_FOR_TIMEZONE;
          settimeofday(&aTimePckt,0);
          timeSStatus= TS_SET;
      // }
    //   else{
    //     timeSStatus= TS_WAITING_FOR_TIMEZONE;
    // }
    }
  }
}
//------------------------------------------------------------------------------------------------
bool isItTimeNow(){
  bool fire= false;  time_t now;  time(&now);
  double someSeconds= difftime(now,previousTimestamp);
  // DAD
  // Serial.printf("Seconds elapsed: %f\r\n",someSeconds);
  if (someSeconds>GPS_UPDATE_IVAL_S){
    previousTimestamp= now;    fire= true;
  }
  // DAD
  // Serial.printf("Fire variable: %d\r\n",fire);
  return fire;
}
//------------------------------------------------------------------------------------------------
void waitForUserInput(){
  bool userPresent= false;
  while (!userPresent){
    // if (Serial.available()) {
    //   Serial.read();
    // }
    Serial.flush();
    Serial.print(F("Press Y key..."));
    while (!Serial.available()) {
      delay(512);
    }
    char aChar= Serial.read();
    if (aChar=='y'){userPresent=true;}
  }
}
//------------------------------------------------------------------------------------------------
void printSpecialCString(char* aStringM, bool hexM, bool oneMoreM){
  // This excludes null terminator
  uint8_t strLength= strlen(aStringM);
  char aChar;
  // uint8_t lastIndex= strLength
  if(oneMoreM){strLength++;}

  for (uint8_t k=0;k<=strLength;k++){
    aChar= aStringM[k];
    if (hexM){
      Serial.print("-"); Serial.print(aChar,HEX);
    } else {
      if (aChar > 31){
        Serial.print(aChar);
      } else{
        Serial.print("-");
        // Serial.print(atoi(&aChar));
        Serial.printf("%x",aChar);
      }
    }
  }
}
//------------------------------------------------------------------------------------------------
  /*
void printSpecialString(String& aStringM){
  uint8_t strLength= aStringM.length();
  char aChar;
  for (uint8_t k=0;k<strLength;k++){
    aChar= aStringM.charAt(k);
    // Serial.print(aChar,HEX);
    if (aChar > 31){
      Serial.print(" "); Serial.print(aChar);
    } else{
      Serial.print(atoi(&aChar));
    }
  }
}
*/
//------------------------------------------------------------------------------------------------
void assembleDataCStr(char* aCStringM,float temperatureM,float humidityM){
  char temperatureCStr[8]; char humidityCStr[8];

  strcat(aCStringM,",");
  sprintf(temperatureCStr,"%g",temperatureM);
  sprintf(humidityCStr,"%g",humidityM);
  strcat(aCStringM,temperatureCStr);
  strcat(aCStringM,",");
  strcat(aCStringM,humidityCStr);
}
//------------------------------------------------------------------------------------------------
void overwriteSpecialCString(char* aCStringM, uint8_t lengthM){
  for (uint8_t k=0;k<=lengthM;k++){
    aCStringM[k]= '#';
  }
}