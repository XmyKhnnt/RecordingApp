import pyaudio
import wave
import os
from pydub import AudioSegment

class AudioHandler:
    def __init__(self, channels=2, rate=44100, chunk=1024, audio_device=0):
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
    
    def start_recording(self, path, filename):
        if self.recording:
            print("Already recording!")
            return
        
        self.recording = True
        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input_device_index=self.audio_device_index,
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
        
        # Convert the recorded audio from WAV to MP3 format
        audio_segment = AudioSegment(
            data=b''.join(self.frames),
            sample_width=self.p.get_sample_size(pyaudio.paInt16),
            frame_rate=self.rate,
            channels=self.channels
        )
        audio_segment.export(os.path.join(path, filename), format='mp3')
        
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
