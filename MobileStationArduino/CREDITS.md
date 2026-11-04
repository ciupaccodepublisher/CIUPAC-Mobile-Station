## Third-Party Licenses

This project is distributed as source code only. The libraries below are **not** included in this repository: PlatformIO downloads them when the firmware is built, and each one is distributed with its own license text.

### Libraries used

1. **Arduino core for ESP32 (arduino-esp32)**
   - Copyright © the arduino-esp32 authors (Espressif Systems and contributors).
   - Licensed under the GNU Lesser General Public License v2.1 (LGPL-2.1).
   - Source: https://github.com/espressif/arduino-esp32

2. **BluetoothSerial** (library bundled with arduino-esp32)
   - Copyright © 2018 Evandro Luis Copercini.
   - Licensed under the Apache License, Version 2.0.

3. **Adafruit DHT sensor library**
   - Copyright © Adafruit.
   - Licensed under the MIT License (the copyright and permission notice of the library must be kept in its copies).
   - Source: https://github.com/adafruit/DHT-sensor-library

4. **Adafruit Unified Sensor**
   - Copyright © Adafruit.
   - Licensed under the Apache License, Version 2.0.
   - Source: https://github.com/adafruit/Adafruit_Sensor

5. **ESP-IDF** (Espressif IoT Development Framework, on which the Arduino core for ESP32 is built)
   - Copyright © Espressif Systems (Shanghai) Co., Ltd.
   - Licensed under the Apache License, Version 2.0.
   - Source: https://github.com/espressif/esp-idf

### Code adapted from public examples

Some lines of `src/main.cpp` follow the examples below:

1. **SerialToSerialBT** example of arduino-esp32 (Bluetooth configuration checks, `#error` lines)
   - By Evandro Copercini, 2018.
   - Released into the Public Domain (or CC0, at your option).

2. **DHTtester** example of the Adafruit DHT sensor library (`DHTTYPE` definition and the comments of `dhtMeasure()`)
   - Written by ladyada.
   - Released into the public domain.

3. **ESP32 with NEO-6M GPS Module (Arduino IDE)**, Random Nerd Tutorials (GPS serial port definitions and setup: `RXD2`, `TXD2`, `GPS_BAUD`, `gpsSerial`)
   - By Rui Santos & Sara Santos - Random Nerd Tutorials.
   - Source: https://randomnerdtutorials.com/esp32-neo-6m-gps-module-arduino/
   - The code of that tutorial carries a permission notice (MIT style) which requires its copyright and permission notice to be included in copies or substantial portions of the code.
