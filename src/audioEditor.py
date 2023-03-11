from pydub import AudioSegment
import os

class AudioTrimmer:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.trimmed_files = []
        self.combined_file = None
        self.trimFolder = f"{self.folder_path}/trimmedFiles"
        self.output_folder = self.folder_path

    def trim_files(self, end_time, start_time=0):
        try:
            # delete existing trimmed files
            if os.path.exists(self.trimFolder):
                for file in os.listdir(self.trimFolder):
                    os.remove(os.path.join(self.trimFolder, file))
            
            for file in os.listdir(self.folder_path):
                
                if file.endswith(".wav") and file.startswith("frame"):
                    print(f"{file}")
                    # load the audio file
                    audio = AudioSegment.from_file(os.path.join(self.folder_path, file))
                    
                    end_time_initial = len(audio) - (end_time * 1000)
                    print(f"  end_time_initial {end_time_initial}")
                    print(f"len(audio) {len(audio)}")

                    # trim the audio file
                    trimmed_audio = audio[start_time:end_time_initial]

                    # export the trimmed audio to a new file
                    print(self.trimFolder)
                    if not os.path.exists(self.trimFolder):
                        os.mkdir(self.trimFolder)

                    trimmed_file = os.path.join(self.trimFolder, f"{file}")

                    trimmed_audio.export(trimmed_file, format=file.split(".")[-1])

                    self.trimmed_files.append(trimmed_file)
        except:
            pass

    def combine_files(self, dir_path):

        if not self.trimmed_files:
            print("No trimmed files found.")
            return
        
        try:
            # delete existing combined file
            if self.combined_file and os.path.exists(self.combined_file):
                os.remove(self.combined_file)
            
            # load the first audio file
            combined_audio = AudioSegment.from_file(self.trimmed_files[0])

            # concatenate the rest of the audio files
            for file in self.trimmed_files[1:]:
                audio = AudioSegment.from_file(file)
                combined_audio += audio

            # export the combined audio to a new file
            self.combined_file = os.path.join(dir_path, "combined_file.wav")
            combined_audio.export(self.combined_file, format="wav")
        except:
            pass
