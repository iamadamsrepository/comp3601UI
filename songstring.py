import tkinter as tk

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