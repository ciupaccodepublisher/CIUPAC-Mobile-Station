// DAD
// Serial.print(F(""));
// Arduino section

// INFO: False == 0
// INFO: With SafeStrings (c++ strings), doing str0= str1 will copy the content of str1 on str0
//       That means that is not a pointer copy, modifying str1 content after assignment will not change
//       str0 content.
// #define DHT_TEST

#define NAME "CIUPAC-MS-00"

#define GPS_ENABLED
#define BT_PRESENT
#define ON_LED

#include <Arduino.h>
#include "DHT.h"
#include "./Utils.hpp"

#ifdef GPS_ENABLED
  #define RXD2 16
  #define TXD2 17
  #define GPS_BAUD 9600
  // Create an instance of the HardwareSerial class for Serial 2
  HardwareSerial gpsSerial(2);
#endif

#define DHTPIN 5
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

#ifdef ON_LED
  #define LEDPIN 22
#endif

enum CommunicationStatus{
  CS_WAITING_FOR_TIME_PACKET,
  CS_READY
};

//------------------------------------------------------------------------------------------------
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
#if !defined(CONFIG_BT_SPP_ENABLED)
  #error Serial Bluetooth not available or not enabled. It is only available for the ESP32 chip.
#endif
 
const char *pin = "1234"; // Change this to more secure PIN.
String device_name = NAME;
String MAC_Address;
CommunicationStatus commStatus;

// WARNING: I don't understand why variables declared in header file generates
// multiple definition error
extern BluetoothSerial serialBT;
DHT dht(DHTPIN, DHTTYPE);
extern TimeSettingStatus timeSStatus;
extern timeval aTimePckt;
extern time_t previousTimestamp;

bool checkNewPacket= false;
const String gpggaStr= "$GPGGA";
float humidity; float temperature;
String aCPPString, gpsData, btReceivedMsg;
#define MSG_CSTR_LENGTH 128
char aCString[MSG_CSTR_LENGTH];
//------------------------------------------------------------------------------------------------
void setup() {

  #ifdef ON_LED
    pinMode(LEDPIN,OUTPUT);
    digitalWrite(LEDPIN,HIGH);
  #endif

  Serial.begin(115200);
  // MAD
  delay(1000); //Take some time to open up the Serial Monitor

  #ifdef GPS_ENABLED
    // Start Serial 2 with the defined RX and TX pins and a baud rate of 9600
    gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);
    gpsSerial.flush();
  #endif

  // waitForUserInput();

  serialBT.enableSSP();
  serialBT.begin(device_name); //Bluetooth device name
  // MAD
  // Serial.printf("The device with name \"%s\" is started.\r\nNow you can pair it with Bluetooth!\r\n", device_name.c_str());
  // serialBT.setPin(pin); Serial.println("Using PIN");
  MAC_Address = serialBT.getBtAddressString();
  aTimePckt.tv_sec= 0;  aTimePckt.tv_usec= 0; settimeofday(&aTimePckt,0);

  dht.begin();
}
//------------------------------------------------------------------------------------------------
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
bool dhtMeasure(){
  humidity = dht.readHumidity();
  // Read temperature as Celsius (the default)
  temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    // Serial.println(F("Failed to read from DHT sensor!"));
    return false;
  } else {return true;};
  // MAD
//   Serial.print(F("Humidity: "));
}
//------------------------------------------------------------------------------------------------
// DAD
// uint8_t counter=0;
void loop() {
  #ifdef GPS_ENABLED
    if (checkNewPacket){
      if (dhtMeasure()){
        bool isAGGAString, weGotAtLeastOneGGAMsg=false;
        while (gpsSerial.available() > 0){
          aCPPString= gpsSerial.readStringUntil('\n');
          isAGGAString= aCPPString.startsWith(gpggaStr);
          // WARNING: This can be used if there are no null chars in string
          // int isAGGAString= strncmp(aCString.c_str(), gpggaStr.c_str(), gpggaStr.length());
          // int isAGGAString= strncmp(aCString, gpggaStr, strlen(gpggaStr));
          if (isAGGAString){
            weGotAtLeastOneGGAMsg= true;
            // DAD
            // Serial.println("++");
            // Serial.println(aCPPString);
            gpsData= aCPPString;
            // Serial.println("--");
            // Serial.println(gpsData);
          }
        }
        if (weGotAtLeastOneGGAMsg){
          // DAD
          Serial.println("----------------------------------------------");
          // -24-47-50-47-47-41-2C-2C-2C-2C-2C-2C-30-2C-30-30-2C-39-39-2E-39-39-2C-2C-2C-2C-2C-2C-2A-34-38-D-0
          // Original string send by GPS ends with \r\n. This removes the "\r".
          gpsData.remove(gpsData.length()-1);
          // -24-47-50-47-47-41-2C-2C-2C-2C-2C-2C-30-2C-30-30-2C-39-39-2E-39-39-2C-2C-2C-2C-2C-2C-2A-34-38-0
          strcpy(aCString,gpsData.c_str());
          assembleDataCStr(aCString,temperature,humidity);
          #ifdef BT_PRESENT
            serialBT.print(aCString);
          #endif
          // DAD
          // Serial.print(F("->: "));
          // Serial.printf("-> (%d): ", counter); counter++;
          // Serial.println(aCString);
          // Clearing GPS input buffer. This means we want just one GPGGA packet each time we check.
          // WARNING: flush() does NOT clear an input buffer.
          // gpsSerial.flush();
          // while (gpsSerial.available() > 0){gpsSerial.read();}
        }
      }
      checkNewPacket= false;
    } else {
      checkNewPacket= isItTimeNow();
      if (checkNewPacket){
          gpsSerial.flush();
          // DAD
          #ifdef ON_LED
            // digitalWrite(LEDPIN,!digitalRead(LEDPIN));
          #endif
      }
    }
  #endif

  #ifdef DHT_TEST
        if (dhtMeasure()){
            Serial.println("--------------------------------------------");
            String anotherString= "a";
            anotherString= anotherString + "b";
            Serial.print(F("->: ")); Serial.println(anotherString);
            aCString= "Uff...: ";
            aCString= aCString +","+ String(temperature) + "," + String(humidity);
            Serial.println(aCString);
            delay(4096);
        }
  #endif

  #ifdef BT_PRESENT
    if (serialBT.available()) {
      btReceivedMsg= serialBT.readStringUntil('\n');
      processReceivedStr(btReceivedMsg);
    }
  #endif
}
//------------------------------------------------------------------------------------------------
