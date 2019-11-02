import tkinter as tk
from PIL import Image, ImageTk

class NoteView:
    def __init__(self, frame, note):
        self.canvas = tk.Canvas(frame, width=60, height=200, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_text(15, 190, text=note)
        self.note = note
        self.notePosition = self.getNotePosition()
        self.noteType = int(note[0])
        self.dotted = self.isDotted()
        self.extraLines = self.needExtras()
        self.image = self.getImage()
        self.addlines()
        self.canvas.image = ImageTk.PhotoImage(Image.open(self.image))
        self.placeImage()

    def addlines(self):
        step = 18
        end = 7*step
        start = 3*step
        curr = start
        while curr <= end:
            self.canvas.create_line(0, curr, 60, curr)
            curr += step

        if self.extraLines > 0:
            self.canvas.create_line(15, 2*step, 45, 2*step)
            if self.extraLines > 1:
                self.canvas.create_line(15, step, 45, step)
        if self.extraLines < 0:
            self.canvas.create_line(10, 8*step, 50, 8*step)

    def getNotePosition(self):
        note = ord(self.note[1]) - ord('a')
        if 0 <= note <= 0:
            position = 0
        elif 1 <= note <= 2:
            position = 1
        elif 3 <= note <= 4:
            position = 2
        elif 5 <= note <= 5:
            position = 3
        elif 6 <= note <= 7:
            position = 4
        elif 8 <= note <= 9:
            position = 5
        elif 10 <= note <= 11:
            position = 6
        elif 12 <= note <= 12:
            position = 7
        elif 13 <= note <= 14:
            position = 8
        elif 15 <= note <= 16:
            position = 9
        elif 17 <= note <= 17:
            position = 10
        elif 18 <= note <= 19:
            position = 11
        elif 20 <= note <= 21:
            position = 12
        elif 22 <= note <= 23:
            position = 13
        elif 24 <= note <= 24:
            position = 14
        else:
            position = 15
        return position

    def getImage(self):
        if self.noteType == 1:
            type = 'semiquaver'
        elif self.noteType == 2:
            type = 'quaver'
        elif self.noteType == 3:
            type = 'crotchet'
        elif self.noteType == 4:
            type = 'minim'
        elif self.noteType == 5:
            type = 'minim'
        elif self.noteType == 6:
            type = 'semibreve'
        if self.notePosition == 15:
            return f'images/rest_{type}.png'
        elif self.noteType == 6:
            return 'images/semibreve.png'
        elif self.notePosition <= 6:
            return f'images/{type}_up.png'
        else:
            return f'images/{type}_down.png'

    def getImagePosition(self):
        y = 0
        if self.notePosition == 15:
            if self.noteType <= 2:
                y = 78
            if self.noteType == 3:
                y = 75
            if 4 <= self.noteType <= 5:
                y = 92
            elif self.noteType == 6:
                y = 83
        elif self.noteType == 6:
            y = 134 - 9 * self.notePosition
        elif self.notePosition <= 6:
            if self.noteType <= 2:
                y = 84 - 9 * self.notePosition
            else:
                y = 83 - 9 * self.notePosition
        else:
            y = 134 - 9 * self.notePosition

        return y


    def placeImage(self):
        # self.canvas.image = ImageTk.PhotoImage(self.image)
        # up - 74 92 110 - 'sw'
        # down - 'nw'
        y = self.getImagePosition()
        self.canvas.create_image(17, y, anchor='nw', image=self.canvas.image)
        if self.dotted:
            self.placeDot()

    def placeDot(self):
        if self.notePosition == 15:
            self.canvas.create_oval(46, 100, 51, 105, fill='black')
        else:
            self.canvas.create_oval(46, 137 - 9 * self.notePosition, 51, 142 - 9 * self.notePosition, fill='black')

    def isDotted(self):
        if self.noteType == 5:
            return True
        return False

    def needExtras(self):
        if 13 <= self.notePosition <= 14:
            return 2
        elif 11 <= self.notePosition <= 12:
            return 1
        elif 0 <= self.notePosition <= 1:
            return -1
        else:
            return 0