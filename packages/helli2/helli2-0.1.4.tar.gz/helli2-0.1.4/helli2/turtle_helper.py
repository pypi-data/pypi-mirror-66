import turtle as t
import png

def islamic_draw(repeat, rotation, pencolor, fillcolor, function, *args):
    t.speed(1)
    t.up()
    t.home()
    t.down()
    t.color(pencolor, fillcolor)
    for i in range(repeat):
        t.begin_fill()
        function(*args)
        t.end_fill()
        t.left(rotation)
    t.color("black", "black")
    t.up()
    t.home()
    t.down()

def create_image(width, height, pixels, name="Untitled"):
    img = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(pixels[i][j][0])
            row.append(pixels[i][j][1])
            row.append(pixels[i][j][2])
        img.append(row)
    with open(name + ".png", mode='wb') as f:    
        w = png.Writer(width, height, greyscale=False)
        w.write(f, img)
        print("Image Created!")
            

def fullscreen():
    scr = t.getscreen()
    scr.cv.master.wm_attributes('-fullscreen','true')
    t.onkey(_exit, "Escape")
    
def _exit():
    t.bye()
    quit()
    
    
def create_button(x, y, func, *args, **kwargs):
    tur = t.Turtle()
    tur.up()
    tur.goto(x, y)
    tur.shape("square")
    
    width = 20
    if("width" in kwargs.keys()):
        width = kwargs["width"]
    
    height = 20    
    if("height" in kwargs.keys()):
        height = kwargs["height"]
        
    tur.shapesize(height / 20.0, width / 20.0)
    
    if("color" in kwargs.keys()):
        tur.color(kwargs["color"])
    
    def func_wrapper(x, y):
        func(*args)
        
    tur.onclick(func_wrapper)