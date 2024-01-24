#############################################
# DrawOnDesk - v1.0.0                       #
# Made by : Aloïs "Shirikoo" Kernaonet      #
# Date : 25.01.2024                         #
# Free app, and feel free to use the code   #
# My discord : shirikoo                     #
# <3                                        #
#############################################

from tkinter import Tk, Toplevel, Canvas, Button, Label, SUNKEN, RAISED, Frame, PhotoImage

class DODFrame():
    def __init__(self, frontWin, backWin, t_color):
        self.front = Frame(frontWin, bg=t_color)
        self.back = Frame(backWin, bg="white")

    def pack(self, packSide):
        self.front.pack(side=packSide)
        self.back.pack(side=packSide)


class DODLabel():
    global LABEL_ICON_DATA, labelFont

    labelFont = ("Tekton Pro", 9, "bold")
    LABEL_ICON_DATA = {
    'size_l': ['button/sizeLabel50x50.png', None]
    }

    def __init__(self, dodframe, content, imageName, position, t_color):
        self.bg = Label(dodframe.front,image=self.getIcon(imageName), bg=t_color, border=0).grid(row=position, column=0)
        Label(dodframe.back, image=self.getIcon(imageName), bg=t_color, border=0).grid(row=position, column=0)
        self.front = Label(dodframe.front, text = content, bg="white", border=0, font=labelFont)
        self.front.grid(row=position, column=0)
        Label(dodframe.back, text = "size", bg="white", border=0).grid(row=position, column=0)

    def getIcon(self, id):
        if id in LABEL_ICON_DATA:
            if LABEL_ICON_DATA[id][1] is None:
                LABEL_ICON_DATA[id][1] = PhotoImage(file=LABEL_ICON_DATA[id][0])
            return LABEL_ICON_DATA[id][1]
        return None

    def setContent(self, content):
        self.front['text']=content


class DODButton():
    global BUTTON_ICON_DATA

    BUTTON_ICON_DATA = {
    'red_b': ['button/redButton60x60.png', None],
    'green_b': ['button/greenButton60x60.png', None],
    'blue_b': ['button/blueButton60x60.png', None],
    'white_b': ['button/whiteButton60x60.png', None],
    'erase_b': ['button/eraseButton50x50.png', None],
    'clear_b': ['button/clearButton50x50.png', None],
    'close_b': ['button/closeButton50x50.png', None],
    'activ_b': ['button/activ50x50.png', None],
    'unactiv_b': ['button/unactiv50x50.png', None],
    'toright_b': ['button/toRightButton50x50.png', None],
    'toleft_b': ['button/toLeftButton50x50.png', None]
    }

    def __init__(self, dodframe, t_color, imageName, position, func, *arg):
        self.visible = Button(dodframe.front, image=self.getIcon(imageName), bg=t_color, border=0, command=lambda: func(*arg), activebackground=t_color)
        self.visible.grid(row=position, column=0)
        self.fonctionnal = Button(dodframe.back, image=self.getIcon(imageName), bg="white", border=0, command=lambda: [func(*arg), self.buttonClickedEffect()])
        self.fonctionnal.grid(row=position, column=0)

    def getIcon(self, id):
        if id in BUTTON_ICON_DATA:
            if BUTTON_ICON_DATA[id][1] is None:
                BUTTON_ICON_DATA[id][1] = PhotoImage(file=BUTTON_ICON_DATA[id][0])
            return BUTTON_ICON_DATA[id][1]
        return None
    
    def buttonClickedEffect(self):
        self.visible.config(relief=SUNKEN)
        self.visible.after(50, lambda: self.visible.config(relief=RAISED))

    def setCommand(self, func, *args):
        self.visible['command'] = lambda: func(*args)
        self.fonctionnal['command'] = lambda: [func(*args), self.buttonClickedEffect]

    def setImage(self, id):
        self.visible['image'] = self.getIcon(id)
    

class drawOnDesk(Tk):
    global points, lineOptions, sizeIndicatorFont, TRANSPARENT_COLOR
    
    line = None
    points = []
    lineOptions = {"fill":"red", "width":5.0}
    sizeIndicatorFont = ("Tekton Pro", 9, "bold")
    TRANSPARENT_COLOR = 'grey15'

    def __init__(self):
        super().__init__()
        self.attributes('-alpha', 0.01)
        self.attributes('-topmost', True)
        self.attributes('-fullscreen', True)
        self.title("DrawOnDesk")
        self.iconphoto(True, PhotoImage(file='icon/dod50x50.png'))

        self.front = Toplevel(self)
        self.front.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.front.attributes('-topmost', True)
        self.front.attributes('-fullscreen', True)
        self.front.title("DrawOnDesk")
        self.front.group(self)
        
        self.canvas = Canvas(self.front, bg=TRANSPARENT_COLOR, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.optionsFrame = DODFrame(self.canvas, self, TRANSPARENT_COLOR)
        self.optionsFrame.pack("left")

        self.redButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'red_b', 0, self.changeColorTo, "red")
        self.blueButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'blue_b', 1, self.changeColorTo, "blue")
        self.greenButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'green_b', 2, self.changeColorTo, "green")
        self.whiteButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'white_b', 3, self.changeColorTo, "white")
        self.activButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'activ_b', 4, self.deactivateScreen)
        self.sizeIndicator = DODLabel(self.optionsFrame, lineOptions['width'], 'size_l', 5, TRANSPARENT_COLOR)
        self.eraserButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'erase_b', 6, self.changeColorTo, TRANSPARENT_COLOR)
        self.clearButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'clear_b', 7, self.clearScreen)
        self.closeButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'close_b', 8, self.closeWin)
        self.changeSideButton = DODButton(self.optionsFrame, TRANSPARENT_COLOR, 'toright_b', 9, self.goToRight)

        self.bind('<Button-1>', self.setFirst)
        self.bind('<B1-Motion>', self.draw)
        self.bind('<ButtonRelease-1>', self.clearPoints)
        self.bind("<MouseWheel>", self.changeSize)
        self.protocol("WM_DELETE_WINDOW", self.closeWin())
        self.front.protocol("WM_DELETE_WINDOW", self.closeWin())

    def setFirst(self, event):
        points.extend([event.x, event.y])

    def draw(self, event):
        global line
        points.extend([event.x, event.y])
        if len(points) == 4:
            line = self.canvas.create_line(points, **lineOptions)
        else:
            self.canvas.coords(line, points)

    def clearPoints(self, event=None):
        global line
        points.clear()
        line = None

    def activateScreen(self):
        self.deiconify()
        self.activButton.setCommand(self.deactivateScreen)
        self.activButton.setImage('activ_b')

    def deactivateScreen(self):
        self.iconify()
        self.activButton.setCommand(self.activateScreen)
        self.activButton.setImage('unactiv_b')

    def goToRight(self):
        self.optionsFrame.pack("right")
        self.changeSideButton.setCommand(self.goToLeft)
        self.changeSideButton.setImage('toleft_b')

    def goToLeft(self):
        self.optionsFrame.pack("left")
        self.changeSideButton.setCommand(self.goToRight)
        self.changeSideButton.setImage('toright_b')

    def closeWin(self):
        self.quit()

    def clearScreen(self):
        self.canvas.delete('all')

    def changeColorTo(self, color):
        lineOptions["fill"] = color

    def changeSize(self, event):
        if (event.num == 5 or event.delta == -120) and lineOptions["width"] > 0.5:
            lineOptions["width"] -= 0.5
        if (event.num == 4 or event.delta == 120) and lineOptions["width"] < 25.0 :
            lineOptions["width"] += 0.5
        self.sizeIndicator.setContent(lineOptions["width"])

    def changeSizeTo(self, size):
        lineOptions["width"] = size


if __name__ == "__main__":
    app = drawOnDesk()
    app.mainloop()