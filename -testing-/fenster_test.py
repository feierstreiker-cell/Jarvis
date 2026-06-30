import tkinter as tk
import threading
import time

class AssistantUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Assistant")
        self.root.geometry("220x120")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        self.label = tk.Label(
            self.root,
            text="Idle",
            fg="white",
            bg="black",
            font=("Arial", 14)
        )
        self.label.pack(expand=True)

        self.state = "idle"

        self.animate()

    def set_state(self, state):
        self.state = state

    def animate(self):
        if self.state == "listening":
            self.label.config(text="Listening ●")
        elif self.state == "thinking":
            self.label.config(text="Thinking ●●")
        elif self.state == "speaking":
            self.label.config(text="Speaking ●●●")
        else:
            self.label.config(text="Idle")

        self.root.after(400, self.animate)
