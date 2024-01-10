RGB-Matrix-P3.0-64x64 from seengreat:www.seengreat.com
  ======================================
# Instructions
## 1.1、verview
This product RGB Matrix P3.0-64x64 is on-board 4096 full-color display LEDs with 3mm pitch,which supports the use of Raspberry Pi developing board. The product is provided with open development resources, suitable for the electronic makers and the related learners to learn or DIY. <br>  
## 1.2、Features
On-board 64 * 64 = 4096 full-color display LEDs<br>   
3mm pitch, displaying text, animation and colorful image<br>  
Onboard two HUB75 headers, respectively  for signal input and output. It can be cascaded multi-screen<br> 
Providing open development resources and tutorials  for the use of Raspberry Pi<br>  

## 1.3、Specifications
|DIMENSIONS|192mm(Length)*192mm(Width)*15mm(Height)|
|---------------|-------------------------------------------------|
|PIXELS|64*64|
|PITCH|3mm|
|PIXEL FORM|1R1G1B|
|VIEWING ANGLE|≥160°|
|HEADER|HUB75|
|CONTROL TYPE|synchronization|
|DRIVING|1/32 scan|
|POWER SUPPLY|5V/4A|
|POWER PORT|VH4 header input|
# Usage
## 2.1、RGB-Matrix-P3.0-64x64-wiring
### 2.1.1、Usage of demo for Raspberry Pi
This product is mainly used with the main-board of Raspberry Pi, with HUB75 for signal input and output of dot matrix screen. <br>                      
Definitions of Raspberry Pi and wiring pin of signal input interface:<br>

The wiring pins definitions of signal input for Raspberry Pi and RGB LED Matrix Panel as following:<br> 
|Label	|Pins Description	|BCM number |Pins Function	|Label	|Pins Description      |BCM number   |Pins Function|
|-----------|----------------------|----------------|-----------------|-----------|----------------------|-----------------|--------------|
|R1	|R higher bit data	|11	       |SCLK  	|G1	|G higher bit data	|27	|P2|
|B1	|B higher bit data	|7	       |CE1	                |GND	|Ground	                |GND	|GND|
|R2	|R lower bit data	|8	       |CE0	                |G2	|G lower bit data	|9	|MISO|
|B2	|B lower bit data	|10	       |MOSI	|E	|E line selection	|15	|RXD|
|A	|A line selection	|22	       |P3	                |B	|B line selection	|23	|P4|
|C	|C line selection	|24	       |P5	                |D	|D line selection	|25	|P6|
|CLK	|Clock input	|17	       |P0	                |LAT	|Latch pin	|4	|P7|
|OE	|Output enable	|18	       |P1	                |GND	|Ground	|GND	|GND|

Usage of demo<br> 
This display uses the open source code on github to demonstrate. Please access the Raspberry Pi terminal, and then enter the following commands in turn:<br> 
sudo git clone https://github.com/hzeller/rpi-rgb-led-matrix<br> 
cd rpi-rgb-led-matrix<br> 
sudo make<br> 
cd examples-api-use<br> 
sudo ./demo -D 9 --led-rows=64 --led-cols=64<br> 
For more details about the demo, please read the contents of the README.md file carefully.<br> 
Cautions of demo<br> 
_1、Turn off onboard audio_<br> 
Please modify the content of /boot/config.txt into dtparam=audio=off,because the on-board audio and the timing circuitry required by RGB-Matrix cannot be run simultaneously.<br> 
2、Please do not run any programs that run in parallel with the GPIO pins.<br> 
3、Disable the 1-wire interface:raspi-config -> Interface Options -> 1-Wire<br> 
4、Add the isolcpus=3 statement at the end of the /boot/cmdline.txt file, separated by spaces<br> 

## 2.1.2、Usage of demo for Rasperry Pi Pico
The wiring pins definitions of signal input for Pico and RGB LED Matrix Panel as following:<br> 
|Label	|Pins Description	|Pico Pins	|Label	|Pin Description	|Pico Pins|
|-----------|----------------------|-----------|-----------|----------------------|----------|
|R1	|R higher bit data	|GP02	|G1	|G higher bit data	|GP03|
|B1	|B higher bit data	|GP04	|GND	|Ground	                |GND|
|R2	|R lower bit data	|GP05	|G2	|G lower bit data	|GP08|
|B2	|B lower bit data	|GP09	|E	|E line selection	|GP22|
|A	|A line selection	|GP10	|B	|B line selection	|GP16|
|C	|C line selection	|GP18	|D	|D line selection	|GP20|
|CLK	|Clock input	|GP11	|LAT	|Latch pin                 |GP12|
|OE	|Output enable	|GP13	|GND	|Ground	                |GND|

_Usage of Demo：_<br>
After wiring the Pico and the display, open the Thonny Python IDE, access the Pico-RGB Matrix LED_64x64 folder in the demo codes in the "File" window (View -> File), and upload all the files and folders in the folder to In Pico, then double-click to open the main.py file, and click the "run" icon in the menu to run the current code.<br>

## 2.1.3、Usage of demo for Arduino Mega
The wiring pins definitions of signal input for Arduino mega and RGB LED Matrix Panel as following:<br> 
|Label       |Pins Description       |Arduino mega Pins	|Label        |Pin Description       |Arduino mega Pins|
|-----------|----------------------|----------------------|-----------|---------------------|---------------------|
|R1	|R higher bit data	|D24	                |G1	|G higher bit data	|D25|
|B1	|B higher bit data	|D26	                |GND	|Ground	                |GND|
|R2	|R lower bit data	|D27	                |G2	|G lower bit data	|D28|
|B2	|B lower bit data	|D29	                |E	|E line selection	|A4|
|A	|A line selection	|A0	                |B	|B line selection	|A1|
|C	|C line selection	|A2	                |D	|D line selection	|A3|
|CLK	|Clock input	|D11	                |LAT	|Latch pin   	|D10|
|OE	|Output enable	|D9	                |GND	|Ground	                |GND|

_Usage of Demo：_<br> 
After wiring the power cable to the display panel and connecting the signal cable according to Table 2-3, access the Arduino_Mega_RGB_Matrix_64x64 folder and double-click to open the Arduino_Mega_RGB_Matrix_64x64.ino file. Then click the Verify button, and then click the Upload button. The demo code realizes the function of displaying text and pictures in a loop<br>    

# Data Resources
https://github.com/hzeller/rpi-rgb-led-matrix<br>


Thank you for choosing the products of Shengui Technology Co.,Ltd. For more details about this product, please visit:
www.seengreat.com 
