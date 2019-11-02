import tkinter as tk


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