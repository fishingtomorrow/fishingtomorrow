import random
import datetime
import ctypes
 
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
 
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
 
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.
 
class Color:
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
     
    def set_cmd_color(self, color, handle=std_out_handle):
        bret = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bret
     
    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
     
    def print_red_text(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()
         
    def print_green_text(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()
     
    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()
           
    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print(print_text)
        self.reset_color()   


print("按回车键开始...")
input()
suc,fail,i = [0,0,0]
begin = datetime.datetime.now()
clr = Color()
while True:
    print("第",i+1, "题：", end = "    ")
    t = random.randint(0,1)
    a = random.randint(0,100)
    res = 0
    if t == 0:
        #加法
        if a == 100:
            b = 0
        else:
            b = random.randint(0,100-a)
        res = a + b
        print(a, "+", b, "=", end = ' ')
    else:
        #减法
        if a == 0:
            b = 0
        else:
            b = random.randrange(0,a)
        res = a - b
        print(a, "-", b, "=", end = ' ')
    user_res = 0
    while True:
        user_res = input()
        if user_res.isdigit():
            break
    if int(user_res) == res:
        clr.print_green_text("正确。\n\f")
        suc = suc + 1
    else:
        clr.print_red_text("错误。\a\n")
        fail = fail + 2
    i = i + 1
    if i % 10 == 0:
        if suc / i * 100 >= 90:
            clr.print_green_text("你的得分："+ str(suc / i * 100)+ " 用时："+ str(datetime.datetime.now() - begin))
        else:
            clr.print_red_text("你的得分："+ str(suc / i * 100)+ " 用时："+ str(datetime.datetime.now() - begin))
        suc,fail,i = [0,0,0]
        print("按回车键开始...")
        input()
        begin = datetime.datetime.now()
