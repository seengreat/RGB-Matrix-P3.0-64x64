import board
import displayio
import framebufferio
import rgbmatrix
from digitalio import DigitalInOut,Direction
import adafruit_display_text.label
import terminalio
from adafruit_bitmap_font import bitmap_font
import time
from math import sin

bit_depth_value = 6
unit_width = 64
unit_height = 64
chain_width = 1
chain_height = 1
serpentine_value = True

width_value = unit_width*chain_width
height_value = unit_height*chain_height

displayio.release_displays()

R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

matrix = rgbmatrix.RGBMatrix(
    width = width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins = [board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
    clock_pin = board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile = chain_height, serpentine=serpentine_value,
    doublebuffer = True)

DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=True,rotation=180)

now = t0 =time.monotonic_ns()
append_flag = 0

class RGB_Api():
    def __init__(self):
        
        #Set image
        self.image = 'wales_128x64.bmp'
        
        #Set text
        self.txt_str = "Raspberry"
        self.txt_color = 0x0000ff
        self.txt_x = 0
        self.txt_y = 32
        self.txt_font = terminalio.FONT
        self.txt_line_spacing = 0.8
        self.txt_scale = 1
        
        #Set scroll
        self.scroll_speed = 30
        
        #The following codes don't need to be set
        self.sroll_BITMAP = displayio.OnDiskBitmap(open(self.image, 'rb'))
        self.sroll_image1 = displayio.TileGrid(
                self.sroll_BITMAP,
                pixel_shader = getattr(self.sroll_BITMAP, 'pixel_shader', displayio.ColorConverter()),
                width = 1,
                height = 1,
                x = 0,
                y = 0,
                tile_width = self.sroll_BITMAP.width,
                tile_height = self.sroll_BITMAP.height)
        self.sroll_image2 = displayio.TileGrid(
                self.sroll_BITMAP,
                pixel_shader = getattr(self.sroll_BITMAP, 'pixel_shader', displayio.ColorConverter()),
                width = 1,
                height = 1,
                x = -self.sroll_BITMAP.width,
                y = -self.sroll_BITMAP.height,
                tile_width = self.sroll_BITMAP.width,
                tile_height = self.sroll_BITMAP.height)
        if self.txt_font == terminalio.FONT:
            self.txt_font = terminalio.FONT
        else:
            self.txt_font = bitmap_font.load_font(self.txt_font)
        self.sroll_text1 = adafruit_display_text.label.Label(
                self.txt_font,
                color = self.txt_color,
                line_spacing = self.txt_line_spacing,
                scale = self.txt_scale,
                text = self.txt_str)
        self.sroll_text1.x = 0
        self.sroll_text1.y = DISPLAY.height//2
        self.sroll_text2 = adafruit_display_text.label.Label(
                self.txt_font,
                color = self.txt_color,
                line_spacing = self.txt_line_spacing,
                scale = self.txt_scale,
                text = self.txt_str)
        self.sroll_text2.x = -self.sroll_text1.bounding_box[2]
        self.sroll_text2.y = DISPLAY.height//2
        
        self.rebound_flag = 0 #Rebound_flag
        self.sroll_object = 0
        
    #@brief:  Display an image in static mode
    #@param:  self
    #@retval: None
    def static_image(self):
        BITMAP = displayio.OnDiskBitmap(open(self.image, 'rb'))
        GROUP = displayio.Group()
        GROUP.append(displayio.TileGrid(
        BITMAP,
        pixel_shader = getattr(BITMAP, 'pixel_shader', displayio.ColorConverter()),
        width = 1,
        height = 1,
        tile_width = BITMAP.width,
        tile_height = BITMAP.height))

        DISPLAY.show(GROUP)
        DISPLAY.refresh()
        while True:
            pass
        
    #@brief:  Display an image from left to right in horizontal mode
    #@param:  self
    #@retval: None
    def image_left_to_right_horizontal(self):
        global append_flag
        self.sroll_image2.y = 0
        x = self.sroll_image1.x + 1
        time.sleep(1/self.scroll_speed)
        if x > self.sroll_BITMAP.width:
            x = 0
        self.sroll_image1.x = x
        self.sroll_image2.x = -(self.sroll_BITMAP.width-self.sroll_image1.x)
        if append_flag == 0:
            append_flag =1
            GROUP.append(RGB.sroll_image1)
            GROUP.append(RGB.sroll_image2)
            DISPLAY.show(GROUP)

    #@brief:  Display an image from right to left in horizontal mode
    #@param:  self
    #@retval: None
    def image_right_to_left_horizontal(self):
        global append_flag
        self.sroll_image2.y = 0
        x = self.sroll_image1.x - 1
        time.sleep(1/self.scroll_speed)
        if x < 0:
            x = self.sroll_BITMAP.width
        self.sroll_image1.x = x
        self.sroll_image2.x = -(self.sroll_BITMAP.width-self.sroll_image1.x)
        if append_flag == 0:
            append_flag =1
            GROUP.append(RGB.sroll_image1)
            GROUP.append(RGB.sroll_image2)
            DISPLAY.show(GROUP)
        
    #@brief:  Display an image from up to down in vertical mode
    #@param:  self
    #@retval: None
    def image_up_to_down_vertical(self):
        global append_flag
        self.sroll_image2.x = 0
        y = self.sroll_image1.y + 1
        time.sleep(1/self.scroll_speed)
        if y > self.sroll_BITMAP.height:
            y = 0
        self.sroll_image1.y = y
        self.sroll_image2.y = -(self.sroll_BITMAP.height-self.sroll_image1.y)
        if append_flag == 0:
            append_flag =1
            GROUP.append(RGB.sroll_image1)
            GROUP.append(RGB.sroll_image2)
            DISPLAY.show(GROUP)
        
    #@brief:  Display an image from down to up in vertical mode
    #@param:  self
    #@retval: None
    def image_down_to_up_vertical(self):
        global append_flag
        self.sroll_image2.x = 0
        y = self.sroll_image1.y - 1
        time.sleep(1/self.scroll_speed)
        if y < 0:
            y = self.sroll_BITMAP.height
        self.sroll_image1.y = y
        self.sroll_image2.y = -(self.sroll_BITMAP.height-self.sroll_image1.y)
        if append_flag == 0:
            append_flag =1
            GROUP.append(RGB.sroll_image1)
            GROUP.append(RGB.sroll_image2)
            DISPLAY.show(GROUP)
    
    #@brief:  Display a text in static mode
    #@param:  self
    #@retval: None
    def static_text(self):
        TEXT = adafruit_display_text.label.Label(
            self.txt_font,
            color = self.txt_color,
            scale = self.txt_scale,
            text = self.txt_str,
            line_spacing = self.txt_line_spacing
            )
        TEXT.x = self.txt_x
        TEXT.y = self.txt_y
        GROUP = displayio.Group()
        GROUP.append(TEXT)
        DISPLAY.show(GROUP)
        DISPLAY.refresh()
        while True:
            pass
        
    
    #@brief:  Display a text from left to right in sinusoidal scrolling mode
    #@param:  self
    #@retval: None
    def text_sin_left_to_right(self):
        global append_flag
        global now
        global t0  
        T = 1/self.scroll_speed
        t_max = t0 + T
        n = 5/self.scroll_speed
        A = 7.5
        Y0 = DISPLAY.height//2
        dt = (now - t0) * 1e-9
        time.sleep(1/self.scroll_speed)
        x = self.sroll_text1.x + 1
        if x > DISPLAY.width:
            x = 0
        self.sroll_text1.x = x
        self.sroll_text2.x = -(DISPLAY.width-self.sroll_text1.x)
        y =  round(Y0 + sin(dt / n) * A)
        self.sroll_text2.y=self.sroll_text1.y = y
        while True:
            now = time.monotonic_ns()
            if now > t_max:
                break
            time.sleep((t_max - now) * 1e-9)
        t_max += T
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)
        
    #@brief:  Display a text from right to left in sinusoidal scrolling mode
    #@param:  self
    #@retval: None
    def text_sin_right_to_left(self):
        global append_flag
        global now
        global t0  
        T = 1/self.scroll_speed
        t_max = t0 + T
        n = 5/self.scroll_speed
        A = 7.5
        Y0 = DISPLAY.height//2
        dt = (now - t0) * 1e-9
        time.sleep(1/self.scroll_speed)
        x = self.sroll_text1.x - 1
        if x < 0:
            x = DISPLAY.width
        self.sroll_text1.x = x
        self.sroll_text2.x = -(DISPLAY.width-self.sroll_text1.x)
        y =  round(Y0 + sin(dt / n) * A)
        self.sroll_text2.y=self.sroll_text1.y = y
        while True:
            now = time.monotonic_ns()
            if now > t_max:
                break
            time.sleep((t_max - now) * 1e-9)
        t_max += T
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)
    
    #@brief:  Display a text from up to down in sinusoidal scrolling mode
    #@param:  self
    #@retval: None
    def text_sin_up_to_down(self):
        global append_flag
        global now
        global t0
        T = 1/self.scroll_speed
        t_max = t0 + T
        n = 5/self.scroll_speed
        A = 5
        X0 = 6
        dt = (now - t0) * 1e-9
        time.sleep(1/self.scroll_speed)
        y = self.sroll_text1.y + 1
        if y > DISPLAY.height:
            y = 0
        self.sroll_text1.y = y
        self.sroll_text2.y = -(DISPLAY.height-self.sroll_text1.y)
        x =  round(X0 + sin(dt / n) * A)
        self.sroll_text2.x=self.sroll_text1.x = x
        while True:
            now = time.monotonic_ns()
            if now > t_max:
                break
            time.sleep((t_max - now) * 1e-9)
        t_max += T
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)

    #@brief:  Display a text from down to up in sinusoidal scrolling mode
    #@param:  self
    #@retval: None
    def text_sin_down_to_up(self):
        global append_flag
        global now
        global t0
        T = 1/self.scroll_speed
        t_max = t0 + T
        n = 5/self.scroll_speed
        A = 5
        X0 = 6
        dt = (now - t0) * 1e-9
        time.sleep(1/self.scroll_speed)
        y = self.sroll_text1.y - 1
        if y < 0:
            y = DISPLAY.height
        self.sroll_text1.y = y
        self.sroll_text2.y = -(DISPLAY.height-self.sroll_text1.y)
        x =  round(X0 + sin(dt / n) * A)
        self.sroll_text2.x=self.sroll_text1.x = x
        while True:
            now = time.monotonic_ns()
            if now > t_max:
                break
            time.sleep((t_max - now) * 1e-9)
        t_max += T
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)
     
    #@brief:  Display a text from left to right in horizontal mode
    #@param:  self
    #@retval: None
    def text_left_to_right_horizontal(self):
        global append_flag
        self.sroll_text1.y=DISPLAY.height//2
        self.sroll_text2.y=DISPLAY.height//2
        x = self.sroll_text1.x + 1
        time.sleep(1/self.scroll_speed)
        if x > DISPLAY.width:
            x = 0
        self.sroll_text1.x = x
        self.sroll_text2.x=-(DISPLAY.width-self.sroll_text1.x)
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)
        
    #@brief:  Display a text from left to right in horizontal mode
    #@param:  self
    #@retval: None
    def text_right_to_left_horizontal(self):
        global append_flag
        self.sroll_text1.y=DISPLAY.height//2
        self.sroll_text2.y=DISPLAY.height//2
        x = self.sroll_text1.x - 1
        time.sleep(1/self.scroll_speed)
        if x < 0:
            x = DISPLAY.width
        self.sroll_text1.x = x
        self.sroll_text2.x=-(DISPLAY.width-self.sroll_text1.x)
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)

    #@brief:  Display a text from up to down in vertical mode
    #@param:  self
    #@retval: None
    def text_up_to_down_vertical(self):
        global append_flag
        self.sroll_text1.x=0
        self.sroll_text2.x=0
        y = self.sroll_text1.y + 1
        time.sleep(1/self.scroll_speed)
        if y > DISPLAY.height:
            y = 0
        self.sroll_text1.y = y
        self.sroll_text2.y=-(DISPLAY.height-self.sroll_text1.y)
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)
        
    #@brief:  Display a text from down to up in vertical mode
    #@param:  self
    #@retval: None
    def text_down_to_up_vertical(self):
        global append_flag
        self.sroll_text1.x=0
        self.sroll_text2.x=0
        y = self.sroll_text1.y - 1
        time.sleep(1/self.scroll_speed)
        if y < 0:
            y = DISPLAY.height
        self.sroll_text1.y = y
        self.sroll_text2.y=-(DISPLAY.height-self.sroll_text1.y)
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            GROUP.append(self.sroll_text2)
            DISPLAY.show(GROUP)

    #@brief:  Display a text in left and right rebound mode
    #@param:  self
    #@retval: None
    def text_rebound_left_and_right(self):
        global append_flag
        self.sroll_text1.y=DISPLAY.height//2
        time.sleep(1/self.scroll_speed) 
        if self.rebound_flag == 0:
            x = self.sroll_text1.x + 1
            if x > DISPLAY.width-self.sroll_text1.bounding_box[2]:
                self.rebound_flag = 1
        else :
            x = self.sroll_text1.x - 1
            if x < 0:
                self.rebound_flag = 0
        self.sroll_text1.x = x
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            DISPLAY.show(GROUP)

    #@brief:  Display a text in up and down rebound mode
    #@param:  self
    #@retval: None
    def text_rebound_up_and_down(self):
        global append_flag
        time.sleep(1/self.scroll_speed)
        if self.rebound_flag == 0:
            y = self.sroll_text1.y + 1
            if y > DISPLAY.height-8:
                self.rebound_flag = 1
        else :
            y = self.sroll_text1.y - 1
            if y < 3:
                self.rebound_flag = 0
        self.sroll_text1.y = y
        if append_flag == 0:
            append_flag =1
            GROUP.append(self.sroll_text1)
            DISPLAY.show(GROUP)
            
    #@brief:  Choose mode
    #@param:  The number of mode
    #@retval: None
    def test(self,mode):
        if mode == 1:
            self.static_image()
        elif mode == 2:
            self.image_left_to_right_horizontal()
        elif mode == 3:
            self.image_right_to_left_horizontal()
        elif mode == 4:
            self.image_up_to_down_vertical()
        elif mode == 5:
            self.image_down_to_up_vertical()
        elif mode == 6:
            self.static_text()
        elif mode == 7:
            self.text_sin_left_to_right()
        elif mode == 8:
            self.text_sin_right_to_left()
        elif mode == 9:
            self.text_sin_up_to_down()
        elif mode == 10:
            self.text_sin_down_to_up()
        elif mode == 11:
            self.text_left_to_right_horizontal()
        elif mode == 12:
            self.text_right_to_left_horizontal()
        elif mode == 13:
            self.text_up_to_down_vertical()
        elif mode == 14:
            self.text_down_to_up_vertical()
        elif mode == 15:
            self.text_rebound_left_and_right()
        elif mode == 16:
            self.text_rebound_up_and_down()

if __name__ == '__main__':
    RGB = RGB_Api()
    GROUP = displayio.Group()
    while True:
        # Number  Function
        #    1    Display an image in static mode           
        #    2    Display an image from left to right in horizontal mode     
        #    3    Display an image from right to left in horizontal mode
        #    4    Display an image from up to down in vertical mode
        #    5    Display an image from down to up in vertical mode
        #    6    Display a text in static mode
        #    7    Display a text from left to right in sinusoidal scrolling mode
        #    8    Display a text from right to left in sinusoidal scrolling mode
        #    9    Display a text from up to down in sinusoidal scrolling mode
        #   10    Display a text from down to up in sinusoidal scrolling mode
        #   11    Display a text from left to right in horizontal mode
        #   12    Display a text from right to left in horizontal mode
        #   13    Display a text from up to down in vertical mode
        #   14    Display a text from down to up in vertical mode
        #   15    Display a text in left and right rebound mode
        #   16    Display a text in up and down rebound mode
        
        #You can select the corresponding function according to the above numbers
        #Example :RGB.test(1) whose function is displaying an image in static mode
        RGB.test(1)
    pass