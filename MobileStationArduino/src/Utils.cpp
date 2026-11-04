// SPDX-License-Identifier: GPL-3.0-or-later
/////////////////////////////////////////////////////////////////////////////////////////////////////
// Copyright (C) 2026 Emiliano Farías <efarias@iado-conicet.gob.ar>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
/////////////////////////////////////////////////////////////////////////////////////////////////////

#include "Utils.hpp"

BluetoothSerial serialBT;
TimeSettingStatus timeSStatus;
timeval aTimePckt;
time_t previousTimestamp=0;

//------------------------------------------------------------------------------------------------
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
