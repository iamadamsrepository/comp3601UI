import tkinter as tk
from noteview import NoteView

class NotationView:
    def __init__(self, frame, stringvar):
        self.frame = tk.Frame(frame)
        self.noteviews = []
        self.buttons = []
        self.stringvar = stringvar
        self.update()
        self.frame.pack()

    def update(self):
        string = self.stringvar.get()
        for i in self.noteviews:
            i.destroy()
        for i in self.buttons:
            i.destroy()

        leftButton = tk.Button(self.frame, text='<', width=4, height=10)
        leftButton.pack(side='left')
        self.buttons.append(leftButton)

        for i in range(2, len(string), 2):
            noteFrame = tk.Frame(self.frame, width=40, height=200, highlightbackground='black', highlightthickness=0)
            noteview = NoteView(noteFrame, string[i-1:i+1])
            noteFrame.pack(side='left')
            self.noteviews.append(noteFrame)

        rightButton = tk.Button(self.frame, text='>', width=4, height=10)
        rightButton.pack(side='left')
        self.buttons.append(rightButton)

    # def destroy(self):
    #     self.frame.destroy()
