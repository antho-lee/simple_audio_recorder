import sounddevice as sd
import numpy as np
import tkinter as tk
from threading import Thread

class AudioRecorder:
    def __init__(self, samplerate=44100, channels=2):
        self.samplerate = samplerate
        self.channels = channels
        self.recording = False
        self.audio_data = np.array([])

    def start_recording(self):
        self.recording = True
        self.audio_data = np.array([])
        stream = sd.InputStream(callback=self.audio_callback, channels=self.channels, samplerate=self.samplerate)
        stream.start()

    def stop_recording(self):
        self.recording = False

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data = np.append(self.audio_data, indata.copy(), axis=0)

    def play_last_10_seconds(self):
        if len(self.audio_data) > 0:
            start_idx = max(0, len(self.audio_data) - self.samplerate * 10)
            sd.play(self.audio_data[start_idx:], self.samplerate)

def record():
    global recorder
    recorder.start_recording()

def stop():
    global recorder
    recorder.stop_recording()

def play():
    global recorder
    recorder.play_last_10_seconds()

recorder = AudioRecorder()

app = tk.Tk()
app.title("Simple Recorder")

record_button = tk.Button(app, text="Record", command=lambda: Thread(target=record).start())
record_button.pack()

stop_button = tk.Button(app, text="Stop", command=stop)
stop_button.pack()

play_button = tk.Button(app, text="Play Last 10s", command=play)
play_button.pack()

app.mainloop()
