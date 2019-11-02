import tkinter as tk
from PIL import Image, ImageTk
import math


class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("COMP3601")
        self.window.geometry("1200x600")

        self.songString = SongString()

        topframe = tk.Frame(self.window, highlightbackground='black', highlightthickness=1)
        topframe.pack(side='top')
        self.top = TopFrame(topframe, self.songString)

        bottomframe = tk.Frame(self.window, highlightbackground='black', highlightthickness=1)
        bottomframe.pack(side='bottom')

        controlframe = tk.Frame(bottomframe, highlightbackground='black', highlightthickness=1)
        controlframe.pack(side='left')

        tempoFrame = tk.Frame(controlframe, highlightbackground='black', highlightthickness=1)
        tempoFrame.pack(side='top')
        self.tempo = TempoControl(tempoFrame)

        lengthsFrame = tk.Frame(controlframe, highlightbackground='black', highlightthickness=1)
        lengthsFrame.pack(side='bottom')
        self.lengths = LengthsChoice(lengthsFrame)

        pianoFrame = tk.Frame(bottomframe, height=200, width=725, highlightbackground='black', highlightthickness=1)
        pianoFrame.pack(side='right')
        self.piano = Piano(pianoFrame, self.songString, self.lengths.var, self.tempo.tempo)

        while True:
            self.updateLoop()
            self.window.update()

    def updateLoop(self):
        self.top.updateNotation()


class SongString:
    def __init__(self):
        self.stringvar = tk.StringVar()
        self.updated = False

    def get(self):
        return self.stringvar.get()

    def set(self, string):
        self.stringvar.set(string)
        self.updated = True

    def update(self):
        self.updated = False

    def needsUpdate(self):
        return self.updated


class TopFrame:
    def __init__(self, frame, songString):
        self.frame = frame
        self.songString = songString
        self.readLabel = tk.Label(self.frame, textvariable=self.songString.stringvar)
        self.readLabel.pack(side='top')
        self.notation = NotationView(self.frame, self.songString)

    def updateNotation(self):
        if self.songString.needsUpdate():
            self.notation.update()
            self.songString.update()


class NotationView:
    def __init__(self, frame, stringvar):
        self.frame = tk.Frame(frame)
        self.noteviews = []
        self.stringvar = stringvar
        self.update()
        self.frame.pack()

    def update(self):
        string = self.stringvar.get()
        for i in self.noteviews:
            i.destroy()
        for i in range(2, len(string), 2):
            noteFrame = tk.Frame(self.frame, width=40, height=200, highlightbackground='black', highlightthickness=0)
            noteview = NoteView(noteFrame, string[i-1:i+1])
            noteFrame.pack(side='left')
            self.noteviews.append(noteFrame)

    def destroy(self):
        self.frame.destroy()


class NoteView:
    def __init__(self, frame, note):
        self.canvas = tk.Canvas(frame, width=60, height=200)
        self.canvas.pack(fill='both')
        self.canvas.create_text(15, 190, text=note)
        self.note = note
        self.notePosition = self.getNotePosition()
        self.noteType = int(note[0])
        self.image = self.getImage()
        self.addlines()
        self.canvas.image = ImageTk.PhotoImage(Image.open(self.image))
        self.placeImage()

    def addlines(self):
        step = 18
        if self.notePosition < 2:
            end = 8*step
        else:
            end = 7*step
        if 10 < self.notePosition < 15:
            start = step
        else:
            start = 3*step

        curr = start
        while curr <= end:
            self.canvas.create_line(0, curr, 50, curr)
            curr += step

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
        elif 24 <= note:
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
            type = 'dottedminim'
        elif self.noteType == 6:
            type = 'semibreve'

        if self.notePosition == 15:
            return f'images/rest-{type}.png'
        elif self.noteType == 6:
            return 'images/semibreve.png'
        elif self.notePosition <= 6:
            return f'images/{type}_up.png'
        else:
            return f'images/{type}_down.png'

    def getImagePosition(self):
        y = 0
        if self.noteType == 6:
            y = 134 - 9 * self.notePosition
        if self.notePosition <= 6:
            y = 83 - 9 * self.notePosition
        else:
            y = 134 - 9 * self.notePosition

        return y


    def placeImage(self):
        # self.canvas.image = ImageTk.PhotoImage(self.image)
        # up - 74 92 110 - 'sw'
        # down - 'nw'
        y = self.getImagePosition()
        self.canvas.create_image(15, y, anchor='nw', image=self.canvas.image)


class Piano:
    def __init__(self, frame, stringvar, lengthsvar, tempovar):
        notes = ['C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4',
                 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5',
                 'C6', 'Rest']
        self.notes = []
        for i, j in zip(notes, range(len(notes))):
            self.notes.append((i, chr(ord('a')+j)))
        self.frame = frame
        self.string = ''
        self.stringvar = stringvar
        self.lengthsvar = lengthsvar
        self.tempovar = tempovar
        for i in self.notes:
            if i[0] == 'Rest':
                self.placeRest()
            else:
                colour = self.getNoteColour(i[0])
                if colour == 'white':
                    text_colour = 'black'
                else:
                    text_colour = 'white'
                coords = self.getNoteCoords(i[0], colour)
                self.placeKey(coords[0], coords[1], colour, text_colour, i[0], i[1])
        # b = tk.Button(frame, height=3, width=2)
        # b.place(x=5, y=26)

    def placeKey(self, x, y, colour, text_colour, text, code):
        button = tk.Button(self.frame, command=lambda: self.pressKey(code), text=text, height=4, width=4, fg=text_colour, highlightbackgroun=colour)
        button.place(x=x, y=y)

    def placeRest(self):
        button = tk.Button(self.frame, command=lambda: self.pressKey('z'), text='Rest', height=2, width=68, fg='black', highlightbackground='white')
        button.place(x=53, y=150)

    def pressKey(self, note):
        self.string = chr(self.tempovar.get()) + str(self.stringvar.get())[1:]
        self.string += str(self.lengthsvar.get())
        self.string += note
        self.stringvar.set(self.string)

    def getNoteColour(self, i):
        if i[1] == 'b':
            return 'black'
        return 'white'

    def getNoteCoords(self, note, colour):
        if colour == 'white':
            x = 5
            y = 75
        else:
            x = -20
            y = 3

        octave = int(note[-1])
        gap = 48
        if octave == 5:
            x += gap * 7
        elif octave == 6:
            x += gap * 7 * 2

        letter = note[0]
        if letter == 'D':
            x += gap
        elif letter == 'E':
            x += gap*2
        elif letter == 'F':
            x += gap*3
        elif letter == 'G':
            x += gap*4
        elif letter == 'A':
            x += gap*5
        elif letter == 'B':
            x += gap*6

        return x, y


class LengthsChoice:
    def __init__(self, frame):
        self.frame = frame
        self.label = tk.Label(frame, text='Crotchet')
        self.label.pack(side='top')
        self.lengths = [(1, '1/4'), (2, '1/2'), (3, '1'), (4, '2'), (5, '3'), (6, '4')]
        self.var = tk.IntVar()
        self.var.set(3)
        for i in reversed(self.lengths):
            c = tk.Radiobutton(frame, text=i[1], variable=self.var, value=i[0], command=lambda: self.updateLabel())
            c.pack(side='bottom')

    def updateLabel(self):
        var = self.var.get()
        if var == 1:
            string = 'Semiquaver'
        elif var == 2:
            string = 'Quaver'
        elif var == 3:
            string = 'Crotchet'
        elif var == 4:
            string = 'Minim'
        elif var == 5:
            string = 'Dotted Minim'
        elif var == 6:
            string = 'Semibreve'
        else:
            string = ''
        self.label.destroy()
        self.label = tk.Label(self.frame, text=string)
        self.label.pack(side='top')


class TempoControl:
    def __init__(self, frame):
        self.label = tk.Label(frame, text='Tempo (60-120 bpm) ')
        self.label.pack(side='left')
        self.entryVal = tk.StringVar()
        self.tempo = tk.IntVar()
        self.tempo.set(60)
        self.entryFrame = tk.Frame(frame)
        self.entryFrame.bind('<Enter>', lambda a: self.checkEntry())
        self.entryFrame.bind('<Leave>', lambda a: self.checkEntry())
        self.entryFrame.pack(side='right')
        self.entry = tk.Entry(self.entryFrame, width=5, textvariable=self.entryVal)
        self.entry.pack()
        self.entry.insert(0, '60')

    def checkEntry(self):
        entry = self.entryVal.get()
        try:
            int(entry)
        except ValueError:
            self.entry.delete(0, len(entry))
            self.entry.insert(0, '60')
        else:
            if int(entry) > 59 and int(entry) < 121:
                self.tempo.set(int(entry))
            else:
                self.entry.delete(0, len(entry))
                self.entry.insert(0, '60')


w = Window()