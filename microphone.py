import pyaudio
import wave
import time
import os

class AudioHandler:
    def __init__(self, channels=2,rate=44100, chunk=1024, audio_device = 0):
        self.audio_device_index = audio_device
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.paused = False
        self.recording = False
        self.playing = False
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.wf = None
    
    def start_recording(self, path, filename):
        if self.recording:
            print("Already recording!")
            return
        
        self.recording = True
        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=self.channels,
                                  rate=self.rate, input_device_index= self.audio_device_index,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        print("Recording started...")
        
        while self.recording:
            if self.paused:
                continue
            
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        
        self.wf = wave.open(os.path.join(path, filename), 'wb')
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        self.wf.setframerate(self.rate)
        self.wf.writeframes(b''.join(self.frames))
        self.wf.close()
        self.wf = None
        
        print("Recording stopped and saved to", filename)
    
    def pause_recording(self):
        self.paused = True
        print("Recording paused...")
    
    def resume_recording(self):
        self.paused = False
        print("Recording resumed...")
    
    def stop_recording(self):
        if not self.recording:
            print("Not recording!")
            return
        
        self.recording = False
        print("Recording stopping...")
    
    def load_wave_file(self, filename):
        self.wf = wave.open(filename, 'rb')
    
    def start_playback(self,filename):
        self.load_wave_file(filename)
        if not self.wf:
            print("No wave file loaded!")
            return
        
        if self.playing:
            print("Already playing!")
            return
        
        self.playing = True
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.channels,
                                  rate=self.rate,
                                  output=True)
        
        print("Playback started...")
        
        data = self.wf.readframes(self.chunk)
        
        while data and self.playing:
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)
        
        self.stop_playback()
    
    def stop_playback(self):
        if not self.playing:
            print("Not playing!")
            return
        
        self.playing = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
