// testshapes demo for RGBmatrixPanel library.
// Demonstrates the drawing abilities of the RGBmatrixPanel library.
// For 64x64 RGB LED matrix.

// WILL NOT FIT on ARDUINO UNO -- requires a Mega, M0 or M4 board

#include "RGBmatrixPanel.h"
#include "Adafruit_GFX.h"


#include "bit_bmp.h"
#include <string.h>
#include <stdlib.h>

// Most of the signal pins are configurable, but the CLK pin has some
// special constraints.  On 8-bit AVR boards it must be on PORTB...
// Pin 11 works on the Arduino Mega.  On 32-bit SAMD boards it must be
// on the same PORT as the RGB data pins (D2-D7)...
// Pin 8 works on the Adafruit Metro M0 or Arduino Zero,
// Pin A4 works on the Adafruit Metro M4 (if using the Adafruit RGB
// Matrix Shield, cut trace between CLK pads and run a wire to A4).

//#define CLK  8   // USE THIS ON ADAFRUIT METRO M0, etc.
//#define CLK A4 // USE THIS ON METRO M4 (not M0)
#define CLK 11 // USE THIS ON ARDUINO MEGA
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3
#define E   A4

RGBmatrixPanel matrix(A, B, C, D, E, CLK, LAT, OE, false, 64);
//Configure the serial port to use the standard printf function
//start
int serial_putc( char c, struct __file * )
{
  Serial.write( c );
  return c;
}
void printf_begin(void)
{
  fdevopen( &serial_putc, 0 );
}
//end

void setup()
{
  Reginit();
  Serial.begin(115200);
  printf_begin();
  matrix.begin();
  delay(500);
}



void loop()
{
  // Do nothing -- image doesn't change
  Demo();
}

//Reginit
void Reginit()
{
  pinMode(24, OUTPUT); //R1
  pinMode(25, OUTPUT); //G1
  pinMode(26, OUTPUT); //B1
  pinMode(27, OUTPUT); //R2
  pinMode(28, OUTPUT); //G2
  pinMode(29, OUTPUT); //B2
  pinMode(CLK, OUTPUT);
  pinMode(OE, OUTPUT);
  pinMode(LAT, OUTPUT);

  digitalWrite(OE, HIGH);
  digitalWrite(LAT, LOW);
  digitalWrite(CLK, LOW);
  int MaxLed = 64;

  int C12[16] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
  int C13[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0};

  for (int l = 0; l < MaxLed; l++)
  {
    int y = l % 16;
    digitalWrite(24, LOW);
    digitalWrite(25, LOW);
    digitalWrite(26, LOW);
    digitalWrite(27, LOW);
    digitalWrite(28, LOW);
    digitalWrite(29, LOW);
    if (C12[y] == 1)
    {
      digitalWrite(24, HIGH);
      digitalWrite(25, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(27, HIGH);
      digitalWrite(28, HIGH);
      digitalWrite(29, HIGH);
    }
    if (l > MaxLed - 12)
    {
      digitalWrite(LAT, HIGH);
    }
    else
    {
      digitalWrite(LAT, LOW);
    }
    digitalWrite(CLK, HIGH);
    delayMicroseconds(2);
    digitalWrite(CLK, LOW);
  }
  digitalWrite(LAT, LOW);
  digitalWrite(CLK, LOW);

  // Send Data to control register 12
  for (int l = 0; l < MaxLed; l++)
  {
    int y = l % 16;
    digitalWrite(24, LOW);
    digitalWrite(25, LOW);
    digitalWrite(26, LOW);
    digitalWrite(27, LOW);
    digitalWrite(28, LOW);
    digitalWrite(29, LOW);
    if (C13[y] == 1)
    {
      digitalWrite(24, HIGH);
      digitalWrite(25, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(27, HIGH);
      digitalWrite(28, HIGH);
      digitalWrite(29, HIGH);
    }
    if (l > MaxLed - 13)
    {
      digitalWrite(LAT, HIGH);
    }
    else
    {
      digitalWrite(LAT, LOW);
    }
    digitalWrite(CLK, HIGH);
    delayMicroseconds(2);
    digitalWrite(CLK, LOW);
  }
  digitalWrite(LAT, LOW);
  digitalWrite(CLK, LOW);
}

//Clear screen
void screen_clear()
{
  matrix.fillRect(0, 0, matrix.width(), matrix.height(), matrix.Color333(0, 0, 0));
}

/*  @name :  display_Image
 *  @brief:  display an image
 *           The image data is in the "bit_bmp.h"
 *           You can use some tools to get the image data
 *           You can set the data bits which is 8 or 16 and set the MSB first which is true or false on line 1001 of Adafruit_GFX.c
 *  @param:    x   Top left corner x coordinate
 *             y   Top left corner y coordinate
 *         bitmap  byte array with 16-bit color bitmap,the image data is in the "bit_bmp.h"
 *             w   Width of bitmap in pixels
 *             h   Height of bitmap in pixels
 *  @retval: None
 */
void display_Image(int16_t x, int16_t y, const uint16_t bitmap[],int16_t w, int16_t h)
{
  matrix.display_image(x, y, bitmap, w, h);
}


#include "Fonts/FreeSerif9pt7b.h"
#include "Fonts/FreeSerifBoldItalic9pt7b.h"
#include "Fonts/RobotoMono_Thin7pt7b.h"
#include "Fonts/FreeSans9pt7b.h"

/*  @name : display_text
 *  @brief: display a text string
 *  @param:    x            X coordinate in pixels
 *             y            Y coordinate in pixels
 *           *str           Text string
 *            *f            Text font,if you use the default font,the value will be NULL,
 *                                    if you use other font ,you should add header file of font to folder named “Fonts” like this Demo
 *           color          16-bit 5-6-5 Color to draw text with
 *         pixels_size      Desired text size. 1 is default 6x8, 2 is 12x16, 3 is 18x24, etc
 *  
 *  @retval: None
 */
void display_text(int x, int y, char *str, const GFXfont *f, int color, int pixels_size)
{
  matrix.setTextSize(pixels_size);// size 1 == 8 pixels high
  matrix.setTextWrap(false); // Don't wrap at end of line - will do ourselves
  matrix.setFont(f);      //set font
  matrix.setCursor(x, y);
  matrix.setTextColor(color);
  matrix.println(str);
}

void Demo()
{
  screen_clear();
  display_text(-1, 14, "R", &FreeSerif9pt7b, matrix.Color333(7, 0, 0), 1);
  display_text(8, 14, "G", &FreeSerif9pt7b, matrix.Color333(0, 7, 0), 1);
  display_text(19, 14, "B", &FreeSerif9pt7b, matrix.Color333(0, 0, 7), 1);
  display_text(31, 5, "M", NULL, 0x7800, 1);
  display_text(37, 5, "a", NULL, 0xFFE0, 1);
  display_text(42, 5, "t", NULL, 0x07E0, 1);
  display_text(48, 5, "r", NULL, 0X001F, 1);
  display_text(53, 5, "i", NULL, 0x07FF, 1);
  display_text(58, 5, "x", NULL, 0x780F, 1);
  display_text(-1, 30, "P30",&RobotoMono_Thin7pt7b, 0xFFE0, 1);
  display_text(12, 25, ".",NULL, 0xFFE0, 1);
  display_text(21, 30, "6",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(29, 30, "4",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(38, 30, "x",&FreeSans9pt7b , 0x780F, 1);
  display_text(46, 30, "6",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(54, 30, "4",&FreeSerifBoldItalic9pt7b , 0x780F, 1);

  display_text(-1, 14+32, "R", &FreeSerif9pt7b, matrix.Color333(7, 0, 0), 1);
  display_text(8, 14+32, "G", &FreeSerif9pt7b, matrix.Color333(0, 7, 0), 1);
  display_text(19, 14+32, "B", &FreeSerif9pt7b, matrix.Color333(0, 0, 7), 1);
  display_text(31, 5+32, "M", NULL, 0x7800, 1);
  display_text(37, 5+32, "a", NULL, 0xFFE0, 1);
  display_text(42, 5+32, "t", NULL, 0x07E0, 1);
  display_text(48, 5+32, "r", NULL, 0X001F, 1);
  display_text(53, 5+32, "i", NULL, 0x07FF, 1);
  display_text(58, 5+32, "x", NULL, 0x780F, 1);
  display_text(-1, 30+32, "P30",&RobotoMono_Thin7pt7b, 0xFFE0, 1);
  display_text(12, 25+32, ".",NULL, 0xFFE0, 1);
  display_text(21, 30+32, "6",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(29, 30+32, "4",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(38, 30+32, "x",&FreeSans9pt7b , 0x780F, 1);
  display_text(46, 30+32, "6",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  display_text(54, 30+32, "4",&FreeSerifBoldItalic9pt7b , 0x780F, 1);
  delay(6000);

  screen_clear();
  
  display_Image(0, 0, Pikachu2_64x64, 64, 64);
  delay(6000);
}
