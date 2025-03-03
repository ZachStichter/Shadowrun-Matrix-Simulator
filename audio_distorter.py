class AudioDistorter():
    def __init__(self,settings=None) -> None:
        self.target_rms=-15
        if settings==None:
            import pedalboard
            self.settings=[
                      pedalboard.Reverb(room_size=0.1,damping=0.9,wet_level=0.15,dry_level=0.8),
                      pedalboard.HighpassFilter(cutoff_frequency_hz=400),
                      pedalboard.LowpassFilter(cutoff_frequency_hz=2850),
                      pedalboard.Distortion(drive_db=17.5),
                      pedalboard.Bitcrush(),
                      pedalboard.Compressor(threshold_db=self.target_rms)
                      ]
        else:
            self.settings = settings

    def distort(self,input_file,output_file):
        import pedalboard
        from pedalboard.io import AudioFile
        import numpy as np
        import soundfile as sf
        audio,sr = sf.read(input_file)
        current_rms = np.log(np.sqrt(np.mean(audio**2)))
        gain_factor = self.target_rms - current_rms
        self.settings.append(pedalboard.Gain(gain_db=gain_factor))
        board = pedalboard.Pedalboard(self.settings)
        with AudioFile(input_file) as i, AudioFile(output_file,'w',i.samplerate,i.num_channels) as o:
            while i.tell() < i.frames:
                chunk = i.read(i.samplerate)
                effected = board(chunk,i.samplerate,reset=False)
                o.write(effected)
        return output_file

class distort:
    def __init__(self,function=None,retain_modified=False):
        self.function = function
        self.temp_files = []
        self.retain = retain_modified

    def _modify_path(self,filepath):
        from os.path import splitext
        head,ext = splitext(filepath)
        fp = head+'_modified'+ext
        self.temp_files.append(fp)
        return fp

    def _distort_sound(self,filepath):
        d = AudioDistorter()
        modified_filepath = self._modify_path(filepath)
        return d.distort(filepath,modified_filepath)

    def _wrapped_function(self,file):
        if self.function.__name__ == 'playsound':
            return self.function(self._distort_sound(file))

    def __enter__(self):
        return self._wrapped_function
    
    def __exit__(self, type,value,traceback):
        function = self.function
        if not self.retain:
            from os import remove
            for file in self.temp_files:
                remove(file)

if __name__ == '__main__':
    # import pedalboard
    # from pedalboard.io import AudioFile
    # from main import playsound

    # # Make a Pedalboard object, containing multiple audio plugins:
    # # parameters: Reverb(room_size=0.005) Reverb(room_size=0.0015)
    # board = pedalboard.Pedalboard([pedalboard.Bitcrush(),pedalboard.Reverb(room_size=0.1,damping=0.9,wet_level=0.15,dry_level=0.8),pedalboard.Distortion(drive_db=17.5),pedalboard.HighpassFilter(cutoff_frequency_hz=400),pedalboard.LowpassFilter(cutoff_frequency_hz=2850)])

    # # Open an audio file for reading, just like a regular file:
    # with AudioFile(r'C:\Users\Zach\OneDrive - nd.edu\_Actual Documents\research\scripts\250201-shadowrun-matrix-emulator\tones\friday3_test.mp3') as f:
  
    #   # Open an audio file to write to:
    #   with AudioFile(r'C:\Users\Zach\OneDrive - nd.edu\_Actual Documents\research\scripts\250201-shadowrun-matrix-emulator\tones\friday3_test_modified.mp3', 'w', f.samplerate, f.num_channels) as o:
  
    #     # Read one second of audio at a time, until the file is empty:
    #     while f.tell() < f.frames:
    #       chunk = f.read(f.samplerate)
      
    #       # Run the audio through our pedalboard:
    #       effected = board(chunk, f.samplerate, reset=False)
      
    #       # Write the output to our output file:
    #       o.write(effected)


    from main import playsound
    from os import path
    # distorter = AudioDistorter()
    input_file = path.join(path.join(path.dirname(__file__),'tones'),'friday3_test.mp3')
    # output_file = r'C:\Users\Zach\OneDrive - nd.edu\_Actual Documents\research\scripts\250201-shadowrun-matrix-emulator\tones\friday3_test_modified.mp3'
    # distorter.distort(input_file,output_file)

    playsound(input_file)
