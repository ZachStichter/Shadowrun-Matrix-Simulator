class SpeechParser():
    def __init__(self):
        import speech_recognition
        from pydub import AudioSegment
        self.listener = speech_recognition.Recognizer()
        self.listener.pause_threshold = 1.0
        self.mic = speech_recognition.Microphone()
        self.timeout = 60
        self.phrase_cutoff = 60
        self.equilibration = 0.2
        self.unknown_response_text = 'Unknown response. Transcribing nothing.'
        self.unknown_response_exception = speech_recognition.exceptions.UnknownValueError
        self.timeout_exception = speech_recognition.exceptions.WaitTimeoutError
        self.AudioSegment = AudioSegment
        self.AudioData = speech_recognition.AudioData
        #self.normalize = normalize

    def transcribe(self,response=None):
        if response == None:
            response = self.unknown_response_text
        try:
            with self.mic:
                self.listener.adjust_for_ambient_noise(self.mic, duration=self.equilibration)
                audio = self.listener.listen(self.mic,self.timeout, self.phrase_cutoff)
                boosted_audio_pydub = self.AudioSegment(data=audio.get_wav_data(),sample_width=audio.sample_width,frame_rate=audio.sample_rate,channels=1).normalize()+10
                boosted_audio = self.AudioData(boosted_audio_pydub.raw_data,boosted_audio_pydub.frame_rate,boosted_audio_pydub.sample_width)
                text = self.listener.recognize_google(boosted_audio)
        except self.unknown_response_exception as e:
            text = response
        except self.timeout_exception as e:
            text = response
        return text



# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
    
# Loop infinitely for user to
# speak

if __name__ == '__main__':
    # import speech_recognition as sr
    # import pyttsx3
    # # Initialize the recognizer 
    # r = sr.Recognizer() 
    # while True:    
    #     # Exception handling to handle
    #     # exceptions at the runtime
    #     try:
        
    #         # use the microphone as source for input.
    #         with sr.Microphone() as source2:
            
    #             # wait for a second to let the recognizer
    #             # adjust the energy threshold based on
    #             # the surrounding noise level 
    #             r.adjust_for_ambient_noise(source2, duration=0.2)
            
    #             #listens for the user's input 
    #             audio2 = r.listen(source2)
            
    #             # Using google to recognize audio
    #             MyText = r.recognize_google(audio2)
    #             MyText = MyText.lower()

    #             print('Did you say ',MyText)
    #             SpeakText(MyText)
            
    #     except sr.RequestError as e:
    #         print(f'Could not request results; {e}')
        
    #     except sr.UnknownValueError:
    #         print('Unknown error')
    parse = SpeechParser()
    while True:
        try:
            text = parse.transcribe()
            if text == 'exit':
                break
            print(text)
        except Exception as e:
            print(e, type(e))