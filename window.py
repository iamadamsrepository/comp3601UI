import tkinter as tk
from songstring import SongString
from reviewframe import ReviewFrame
from controlframe import TempoControl, LengthsChoice, Piano

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("COMP3601")
        self.window.geometry("1200x600")

        self.songString = SongString()

        topframe = tk.Frame(self.window, highlightbackground='black', highlightthickness=1)
        topframe.pack(side='top')
        self.top = ReviewFrame(topframe, self.songString)

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