from pydub import AudioSegment
import os

class AudioTrimmer:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.trimmed_files = []
        self.combined_file = None

    def trim_files(self, end_time, start_time=0):
        try:
            for file in os.listdir(self.folder_path):
                
                if file.endswith(".wav"):
                    # load the audio file
                    audio = AudioSegment.from_file(os.path.join(self.folder_path, file))
                    
                    end_time_initial = len(audio) - (end_time * 1000)
                    print(f"  end_time_initial {end_time_initial}")
                    print(f"len(audio) {len(audio)}")

                    # trim the audio file
                    trimmed_audio = audio[start_time:end_time_initial]

                    # export the trimmed audio to a new file
                    trimmed_file = os.path.join(self.folder_path, f"trimmed_{file}")
                    trimmed_audio.export(trimmed_file, format=file.split(".")[-1])

                    self.trimmed_files.append(trimmed_file)
        except:
            pass

    def combine_files(self, dir_path):

        if dir_path == "":
            dir_path = self.folder_path

        if not self.trimmed_files:
            print("No trimmed files found.")
            return
        try:
        # load the first audio file
            combined_audio = AudioSegment.from_file(self.trimmed_files[0])

            # concatenate the rest of the audio files
            for file in self.trimmed_files[1:]:
                audio = AudioSegment.from_file(file)
                combined_audio += audio

            # export the combined audio to a new file
            self.combined_file = os.path.join(dir_path, f"{self.folder_path}combined_file.wav")
            combined_audio.export(self.combined_file, format="wav")
        except:
            pass

if __name__ == "__main__":
    folder_path = "audiofile"
    trimmer = AudioTrimmer(folder_path)

    # trim the audio files
    trimmer.trim_files(end_time=2000)

    # combine the trimmed audio files
    trimmer.combine_files()

    print("Trimmed files:", trimmer.trimmed_files)
    print("Combined file:", trimmer.combined_file)
