import time
import Adafruit_SSD1306
import os
from PIL import Image, ImageFont, ImageDraw
import math

class Screen:
    # Raspberry Pi pin configuration:
    RST = 24
    EYE_IMAGE_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)) + '/images/'
    TEXT_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/futura.ttf"
    EXCITED = {"excited1", "excited2", "excited3"}
 
    def __init__(self, clear=True):
                    # Constants
        self.SSD1306_I2C_ADDRESS = 0x3C    # 011110+SA0+RW - 0x3C or 0x3D
        self.SSD1306_SETCONTRAST = 0x81
        self.SSD1306_DISPLAYALLON_RESUME = 0xA4
        self.SSD1306_DISPLAYALLON = 0xA5
        self.SSD1306_NORMALDISPLAY = 0xA6
        self.SSD1306_INVERTDISPLAY = 0xA7
        self.SSD1306_DISPLAYOFF = 0xAE
        self.SSD1306_DISPLAYON = 0xAF
        self.SSD1306_SETDISPLAYOFFSET = 0xD3
        self.SSD1306_SETCOMPINS = 0xDA
        self.SSD1306_SETVCOMDETECT = 0xDB
        self.SSD1306_SETDISPLAYCLOCKDIV = 0xD5
        self.SSD1306_SETPRECHARGE = 0xD9
        self.SSD1306_SETMULTIPLEX = 0xA8
        self.SSD1306_SETLOWCOLUMN = 0x00
        self.SSD1306_SETHIGHCOLUMN = 0x10
        self.SSD1306_SETSTARTLINE = 0x40
        self.SSD1306_MEMORYMODE = 0x20
        self.SSD1306_COLUMNADDR = 0x21
        self.SSD1306_PAGEADDR = 0x22
        self.SSD1306_COMSCANINC = 0xC0
        self.SSD1306_COMSCANDEC = 0xC8
        self.SSD1306_SEGREMAP = 0xA0
        self.SSD1306_CHARGEPUMP = 0x8D
        self.SSD1306_EXTERNALVCC = 0x1
        self.SSD1306_SWITCHCAPVCC = 0x2

        # Scrolling constants
        self.SSD1306_ACTIVATE_SCROLL = 0x2F
        self.SSD1306_DEACTIVATE_SCROLL = 0x2E
        self.SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
        self.SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
        self.SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
        self.SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
        self.SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A
        try:
            # 128x64 display with hardware I2C:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
            # Initialize library.
            self.disp.begin()
            self.width = self.disp.width
            self.height = self.disp.height
            self.screen_image = None


            # Clear display.
            if clear:
                self.disp.clear()
                self.disp.display()
        except:
            print("OLED screen is not connected")

    def loop_text(self,direction, string ='', line = 25, font_size = 16):
        
        length = len(string)
        image = Image.new('1', (self.width, self.height))
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size) 
        draw = ImageDraw.Draw(image)
        size = draw.textsize (string , font = font) 
        
        if(line >= 0 and line <= 45):     
               
            if(size[0] > 128):
                print("The string entered is too long.")
            else:
                if(direction == 'R'):
                    self.stop_scroll()
                    draw.text((1, line),string, font=font, fill=255)
                    self.disp.image(image)
                    self.disp.display()
                    self.right_scroll()

                elif(direction == 'L'):
                    self.stop_scroll()
                    draw.text((1, line),string, font=font, fill=255)
                    self.disp.image(image)
                    self.disp.display()
                    self.left_scroll()

                elif(direction == 'S'):  
                    self.stop_scroll()
        else:
            print('Lines can be entered from 0 to 45.')
            
    def clock(self, hour, minute , string ='', font_size = 16):

        image = Image.new('1', (self.width, self.height))
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size) 
        draw = ImageDraw.Draw(image)
        size = draw.textsize (string , font = font) 
        width = self.disp.width
        height = self.disp.height

        # Clock
        draw.rectangle((0,0,self.disp.width,self.disp.height), outline=0, fill=0)

        # Draw an ellipse.
        draw.ellipse((1, 1 , 64, 64), outline=255, fill=0)
        draw.ellipse((6, 6 , 58, 58), outline=255, fill=0)
        draw.ellipse((31, 31 , 33, 33), outline=255, fill=0)

        Timer_x = 32 
        Timer_y = height/2 

        # minute    
        basicMinHand = 19
        ampMinHand = 0.1

        if(minute <= 15):
            minHand = basicMinHand +(minute * ampMinHand)        
        elif(minute <= 30):
            minHand = basicMinHand +((15-(minute-15)) * ampMinHand)
        elif(minute <= 45):
            minHand = basicMinHand +((minute-30) * ampMinHand)    
        elif(minute <= 60):
            minHand = basicMinHand +((15-(minute-45)) * ampMinHand)

        claMinute = minute * 6 + 270 
        if(claMinute > 360):
            claMinute = claMinute -360

        radMin = 3.14159 /180 * claMinute; 

        x = minHand * math.cos(radMin) + Timer_x; 
        y = minHand * math.sin(radMin) + Timer_y;
        draw.line((Timer_x, Timer_y, x , y), fill=255); 
        #draw.ellipse((x-1, y-1, x+1 , y+1), fill=255);     

        # hour  
        ampmHour = hour

        if(hour > 12):
            hour = hour - 12


        basicHourHand = 15
        ampHourHand = 0.1

        if(hour <= 3):
            hourHand = basicHourHand + (hour * ampHourHand)   
        elif(hour <= 6):
            hourHand = basicHourHand + ((3-(hour-3)) * ampHourHand)
        elif(hour <= 9):
            hourHand = basicHourHand + ((hour-6) * ampHourHand)    
        elif(hour <= 12):
            hourHand = basicHourHand + ((3-(hour-9)) * ampHourHand)

        calHour = (hour * 30 + 270) #+ (6*claMinute/60)
        if(calHour > 360):
            calHour = calHour -360        

        radMin = 3.14159 /180 * calHour; 

        x = hourHand * math.cos(radMin) + Timer_x; 
        y = hourHand * math.sin(radMin) + Timer_y;

        draw.line((Timer_x, Timer_y, x , y), fill=255); 

        # Load default font.
        #font = ImageFont.load_default()
        font = ImageFont.truetype(self.TEXT_FILE_PATH, 15)

        if(ampmHour >= 10):
            if(minute >= 10):
                draw.text((73, 18),str(ampmHour) + ' : ' + str(minute),  font=font, fill=255)
            else:
                draw.text((73, 18),str(ampmHour) + ' : 0' + str(minute),  font=font, fill=255)
        else:
            if(minute >= 10):
                draw.text((73, 18),'  ' + str(ampmHour) + ' : ' + str(minute),  font=font, fill=255)
            else:
                draw.text((73, 18),'  ' + str(ampmHour) + ' : 0' + str(minute),  font=font, fill=255)

        length = len(string)
        if(length > 8):
            print('Please enter 8 characters or fewer than 8 characters.')
        else:
            font = ImageFont.truetype(self.TEXT_FILE_PATH, 12)
            draw.text((69, 18 + 25),string, font=font, fill=255)

        # Display image.
        self.disp.image(image)
        self.disp.display()

    def off(self):
        # self.SSD1306_DISPLAYOFF = 0xAE
        self.disp.command(self.SSD1306_DISPLAYOFF)

    def on(self):
        # self.SSD1306_DISPLAYALLON = 0xA5
        self.disp.command(self.SSD1306_DISPLAYON)

    def normal(self):
        # self.SSD1306_NORMALDISPLAY = 0xA6
        self.disp.command(self.SSD1306_NORMALDISPLAY)

    def invert(self):
        # self.SSD1306_INVERTDISPLAY = 0xA7
        self.disp.command(self.SSD1306_INVERTDISPLAY)

    def stop_scroll(self):
        # self.SSD1306_DEACTIVATE_SCROLL = 0x2E
        self.disp.command(self.SSD1306_DEACTIVATE_SCROLL)

    def start_scroll(self):
        # self.SSD1306_ACTIVATE_SCROLL = 0x2F
        self.disp.command(self.SSD1306_ACTIVATE_SCROLL)

    def right_scroll(self):
        self.disp.command(0x26)#SSD1306_RIGHT_HORIZONTAL_SCROLL
        self.disp.command(0x00)#dummy    
        self.disp.command(0x00)#start
        self.disp.command(0x00)
        self.disp.command(0x0f)#stop
        self.disp.command(0x00)
        self.disp.command(0xff)
        self.start_scroll()

    def left_scroll(self):
        self.disp.command(0x27)#SSD1306_LEFT_HORIZONTAL_SCROLL
        self.disp.command(0x00)#dummy    
        self.disp.command(0x00)#start
        self.disp.command(0x00)
        self.disp.command(0x0f)#stop
        self.disp.command(0x00)
        self.disp.command(0xff)
        self.start_scroll()

    def vert_and_hor_left_scroll(self):
        self.disp.command(0x29)#SSD1306_LEFT_HORIZONTAL_SCROLL
        self.disp.command(0x00)#dummy    
        self.disp.command(0x00)#start
        self.disp.command(0x00)
        self.disp.command(0x0f)#stop
        self.disp.command(0x00)
        self.disp.command(0xff)
        self.disp.command(0x2f)#activate scroll

    def set_contrast(self,value):
        self.disp.set_contrast(value)
        
    #added in 1.3
    def flicker_text(self, string, count=10, delay=0.5):
        if(len(string) > 8):
            print('Please enter 8 characters or fewer than 8 characters.')
        else:
            message = string

            self.clear_display()
            self.draw_text_center(message)
            for i in range(0, count):        
                #self.clear_display() 
                #self.draw_text_center(message)
                self.on()
                time.sleep(delay+0.01)
                self.off() 
                time.sleep(delay+0.01)
            #make sure to turn display back on    
            self.on() 
  

    #added in 1.3
    def size_text(self,count, size, string):
        if(len(string) > 8):
            print('Please enter 8 characters or fewer than 8 characters.')
        else:     
            message = string
            self.draw_text_center(message,font_size=16)    
            
            for i in range(0, count): 
                
                for j in range(16,size,2):            
                    self.draw_text_center(message,font_size=j)
                
                for j in range(size, 16, -2):    
                    self.draw_text_center(message,font_size=j)
    #added in 1.3
    def moving_text(self,direction, string, line = 25, speed = 5,font_size = 16):         

        image = Image.new('1', (self.width, self.height))
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size)   
        draw = ImageDraw.Draw(image)
        
        size = draw.textsize (string , font = font)
        pos = 128 - size[0]    
        length = len(string)
        
        if(line >= 0 and line <= 45):     
               
            if(length > 8):
                print('Please enter 8 characters or fewer than 8 characters.')
            else:      
                if(direction == 'R'):  
                    for i in range(0, pos, speed):
                        image = Image.new('1', (self.width, self.height))
                        draw = ImageDraw.Draw(image)
                        self.disp.display()                
                        draw.text((0 + i, line), string, font=font, fill=255)                
                        self.disp.image(image)
                        self.disp.display()      

                if(direction == 'L'):  
                    for i in range(pos, 0, -speed):
                        image = Image.new('1', (self.width, self.height))
                        draw = ImageDraw.Draw(image)
                        self.disp.display()                
                        draw.text((0 + i, line), string, font=font, fill=255)                
                        self.disp.image(image)
                        self.disp.display()  
        else:
            print('Lines can be entered from 0 to 45.')

    def clear_display(self):
        self.disp.clear()
        self.disp.display()

    def draw_text(self, string, x=1, y=1, display=0, image=0, font_size=16, clear=True):
        if display == 0:
            display = self.disp
        if image == 0:
            image = Image.new('1', (self.width, self.height))
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size)
        draw = ImageDraw.Draw(image)
        max_x = 0
        max_y = 0
        if clear:
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        current_x = x
        current_y = y

        for char in string:
            char_width, char_height = draw.textsize(char, font=font)
            # print(char + ": height-" + str(char_height) + ", width-" + str(char_width))
            max_x = char_width if max_x < char_width else max_x
            max_y = char_height if max_y < char_height else max_y
            draw.text((current_x, current_y), char, font=font, fill=255)
            current_x += char_width
            if current_x > self.width - max_x:
                current_x = x
                current_y += max_y + 1
        display.image(image)
        display.display()

        self.screen_image = image

    def draw_text_center(self, string, display=0, image=0, font_size=16, clear=True):

        words = string.split(' ')
        split_lines = []
        text = ""
        current_h = font_size
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size)

        if display == 0:
            display = self.disp

        if image == 0:
            image = Image.new('1', (self.width, self.height))

        draw = ImageDraw.Draw(image)

        if clear:
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        for word in words:
            new_line = False
            new_line_next_word = ""

            if "\n" in word:
                try:
                    word, new_line_next_word = word.split("\n")
                    new_line = True
                except:
                    print("You should use '\\n' only once in one word")
                    return

            text += word + " "
            text_width, text_height = draw.textsize(text, font=font)

            if word == words[0]:
                current_h = text_height

            if text_width >= 124:
                text = text[:-len(word)-2]
                split_lines.append(text)
                text = word + " "
                current_h += text_height

            if new_line:
                split_lines.append(text[:-1])
                current_h += text_height
                text = new_line_next_word + " "

            if current_h >= 60:
                print("Sentence is too long")
                return

        split_lines.append(text[:-1])

        current_y = (self.height - 4 - current_h) / 2

        for text in split_lines:
            text_width, text_height = draw.textsize(text, font=font)
            current_x = (self.width - text_width) / 2
            draw.text((current_x, current_y), text, font=font, fill=255)
            current_y += text_height

        display.image(image)
        display.display()

        self.screen_image = image

    def path_to_image(self, path):
        return Image.open(path).convert('1')

    def show_image(self,image):
        import cv2
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert it to gray
        small = cv2.resize(gray, (128,64)) # Resize it to fit the screen
        self.draw_image(Image.fromarray(small).convert('1')) # show the picture! 

    def draw_image(self, img, display=0):
        if display == 0:
            display = self.disp
        display.image(img)
        display.display()

    def draw_image_by_path(self, path):
        self.draw_image(self.path_to_image(path))

    def draw_image_by_name(self, name):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + name + ".ppm"))

    def animate(self, preset=None, custom=False):
        preset = self.EXCITED if preset is None else preset
        if not custom:
            for item in preset:
                self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + item + ".ppm"))
        else:
            for item in preset:
                self.draw_image(item)

    def calibrating(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "calibrating.ppm"))

    def calibrated(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "calibrated.ppm"))

    def close_eyes(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "close.ppm"))

    def sleepy_eyes(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleep.ppm"))

    def sleepy_left(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleepyleft1.ppm"))

    def sleepy_right(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleepyright1.ppm"))

    def blink(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral2.ppm"))
        time.sleep(.25)
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "close.ppm"))
        time.sleep(.25)
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral1.ppm"))

    def look_around_open(self):
        self.draw_image_by_name("lookright1")
        time.sleep(2)
        self.close_eyes()
        self.draw_image_by_name("lookleft1")
        time.sleep(1)
        self.close_eyes()
        self.draw_image_by_name("lookright1")
        time.sleep(1)
        self.close_eyes()
        self.hello()
        time.sleep(1)

    def sleeping(self):
        self.draw_image_by_name("close")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z1")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z2")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z3")
        time.sleep(.6)
        self.draw_image_by_name("close")
        time.sleep(.6)

    def look_around(self):
        self.sleepy_eyes()
        time.sleep(2)
        self.close_eyes()
        self.sleepy_left()
        time.sleep(1)
        self.close_eyes()
        self.sleepy_right()
        time.sleep(1)
        self.close_eyes()
        self.sleepy_eyes()
        time.sleep(1)

    def glimmer(self):
        glimmer = ["neutral1", "neutral2", "neutral3"]
        self.animate(glimmer)

    def sad(self):
        sad = ["sad1"]
        #sad = ["sad1", "sad2", "sad3"]
        self.animate(sad)

    def happy(self):
        happy = ["neutral1", "neutral2"]
        wink = ["happy_left2", "happy_right1"]
        self.animate(happy)
        for i in range(3):
            self.animate(wink)
        self.hello()

    def hello(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral1.ppm"))

    def angry(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "focus.ppm"))

    def connection_success(self):
        self.draw_image_by_name("connected")

    def connection_fail(self):
        self.draw_image_by_name("onlinefail")


def run():
    print("test screen.py script")
    eye = Screen()
    print(eye.TEXT_FILE_PATH)
    print(os.path.dirname(os.path.abspath(__file__)))
    eye.draw_text("hello world")
    time.sleep(2)
    eye.close_eyes()
    time.sleep(2)
    eye.blink()
    time.sleep(2)
    eye.glimmer()
    time.sleep(2)
    eye.sad()
    time.sleep(2)
    eye.happy()
    time.sleep(2)
    eye.hello()
    print("end test screen.py")


if __name__ == '__main__':
    run()
