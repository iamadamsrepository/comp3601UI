import tkinter as tk
from notationview import NotationView

class ReviewFrame:
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