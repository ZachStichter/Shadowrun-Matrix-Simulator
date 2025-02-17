class tts_manager():
    def __init__(self):
        try:
            use_elevenlabs = self.start_elevenlabs()
        except Exception as e:
            print(e,type(e))
        if use_elevenlabs:
            self.model = 'elevenlabs'
        else:
            self.model = 'parler'
            from quash_print_output import quash_print_output as quash
            with quash():
                import os
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
                import torch
                from parler_tts import ParlerTTSForConditionalGeneration
                from transformers import AutoTokenizer
                self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
                #self.attn_implementation = 'eager'
                self.parler_model = ParlerTTSForConditionalGeneration.from_pretrained('parler-tts/parler-tts-mini-v1').to(self.device)
                self.tokenizer = AutoTokenizer.from_pretrained('parler-tts/parler-tts-mini-v1')
                self.description = "Laura's synthetic female voice delivers a well-enunciated, slightly monotone statement with moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding as if it were in the listener's head. Her pitch decreases at the end of each sentence."
                self.input_ids = self.tokenizer(self.description, return_tensors='pt').input_ids.to(self.device)
    
    def generate(self, prompt, location):
        if self.model == 'parler':
            self.parler_generate(prompt,location)
        elif self.model == 'elevenlabs':
            self.elevenlabs_generate(prompt,location)
        else:
            print(f"Something's very wrong here. I'm not configured to work with {self.model}. I'm only configured for parler or elevenlabs.")

    def start_elevenlabs(self):
        from elevenlabs.client import ElevenLabs
        import os
        api_key = os.environ.get('ELEVENLABS_API_KEY')
        self.client=ElevenLabs(api_key=api_key)
        self.voice_id = os.environ.get('ELEVENLABS_FRIDAY') # elevenlabs matilda
        self.eleven_model_id = 'eleven_multilingual_v2'
        self.output_format = 'mp3_44100_128'
        try:
            result = self.client.text_to_speech.convert(text='a',voice_id=self.voice_id,model_id=self.eleven_model_id,output_format=self.output_format,)
            result = b''.join(result)
            if len(result) > 0:
                return True
            else:
                return False
        except Exception as e:
            print(e,type(e))
            return False

    def elevenlabs_generate(self, prompt, location):
        from elevenlabs.play import save
        audio_arr = self.client.text_to_speech.convert(text=prompt, voice_id=self.voice_id,model_id=self.eleven_model_id,output_format=self.output_format)
        save(audio_arr,location)

    def parler_generate(self,prompt, location):
        from quash_print_output import quash_print_output as quash
        with quash():
            import soundfile as sf
            self.prompt_ids = self.tokenizer(prompt,return_tensors='pt').input_ids.to(self.device)
            self.generation = self.parler_model.generate(input_ids=self.input_ids, prompt_input_ids=self.prompt_ids)
            audio_arr = self.generation.cpu().numpy().squeeze()
            sf.write(location,audio_arr,self.parler_model.config.sampling_rate)



if __name__ == '__main__':
    # import torch
    # from parler_tts import ParlerTTSForConditionalGeneration
    # from transformers import AutoTokenizer
    # import soundfile as sf
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # attn_implementation = 'eager'

    # model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-large-v1",attn_implementation=attn_implementation).to(device)
    # tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-large-v1")
    # #tokenizer.pad_token = tokenizer.eos_token + "_pad"

    # prompt = 'Logout Successful! ... Returning you to "meat world" in three... two... one'
    # description = "Laura's electronic-sounding female voice delivers a well-enunciated, slightly monotone statement with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up. Her pitch goes down at the end of each sentence. There is nearly no background noise. She emphasizes meat world with special emphasis before counting backwards from three. She breathes in before beginning speaking and waits for a moment after finishing her countdown."

    # input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    # prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    # generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    # audio_arr = generation.cpu().numpy().squeeze()
    # sf.write("250201-shadowrun-matrix-emulator/logout.wav", audio_arr, model.config.sampling_rate)
    from env_manager import load_dotenv

    load_dotenv()

    tts = tts_manager()
    tts.generate('hi','file.mp3')