import pyaudio
import wave
import time
import os


class AudioHandler:
    def __init__(self, channels=1, rate=44100, chunk=1024):
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
                                  rate=self.rate,
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
    
    def start_playback(self, filename):
        if self.playing:
            print("Already playing!")
            return
        
        self.playing = True
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.channels,
                                  rate=self.rate,
                                  output=True)
        self.wf = wave.open(filename, 'rb')
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
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.wf.close()
        self.wf = None
        print("Playback stopped.")
    
    def __del__(self):
        self.p.terminate()

if __name__ == '__main__':
    audio_handler = AudioHandler()

    # Record for 5 seconds
    audio_handler.start_recording()

    # Pause the recording for 2 seconds
    audio_handler.pause_recording()
    time.sleep(2)
 

    # Record for another 5 seconds
    audio_handler.start_recording()

    # Stop the recording
    audio_handler.stop_recording()
