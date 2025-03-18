from typing import Union,Generator,Iterable

class tts_manager():
    def __init__(self):
        self.parler_started = False
        use_playht = False
        try:
            use_elevenlabs, self.client = self.start_elevenlabs()
            if use_elevenlabs:
                self.model = 'elevenlabs'
        except Exception as e:
            #print(e,type(e))
            print('Cannot use elevenlabs. Falling back to PlayHT')
        # try:
        #     if not use_elevenlabs:
        #         use_playht, self.client = self.start_playht()
        #     if use_playht:
        #         self.model = 'playht'
        # except Exception as e:
        #     print(e)
        #     print('Cannot use playht. Falling back to local.')
        if (not use_elevenlabs) and (not use_playht):
            print('Starting local')
            self.model = 'parler'
            self.start_parler()
    
    def generate(self, prompt, location):
        if self.model == 'parler':
            self.parler_generate(prompt,location)
        elif self.model == 'elevenlabs':
            self.elevenlabs_generate(prompt,location)
        elif self.model == 'playht':
            self.playht_generate(prompt,location)
        else:
            print(f"Something's very wrong here. I'm not configured to work with {self.model}. I'm only configured for parler or elevenlabs.")

    def start_elevenlabs(self):
        from elevenlabs.client import ElevenLabs
        import os
        api_key = os.environ.get('ELEVENLABS_API_KEY')
        client=ElevenLabs(api_key=api_key)
        self.voice_id = os.environ.get('ELEVENLABS_FRIDAY') # elevenlabs matilda
        self.eleven_model_id = 'eleven_multilingual_v2'
        self.output_format = 'mp3_44100_128'
        try:
            result = client.text_to_speech.convert(text='a',voice_id=self.voice_id,model_id=self.eleven_model_id,output_format=self.output_format,)
            result = b''.join(result)
            if len(result) > 0:
                return True, client
            else:
                return False, None
        except Exception as e:
            print(e,type(e))
            return False, None

    def elevenlabs_generate(self, prompt, location):
        try:
            audio_arr = self.client.text_to_speech.convert(text=prompt, voice_id=self.voice_id,model_id=self.eleven_model_id,output_format=self.output_format)
            save_audio(audio_arr,location)
        except:
            self.fallback(prompt,location)

    def parler_generate(self,prompt, location):
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        from quash_print_output import quash_print_output as quash
        with quash():
            import soundfile as sf
            if not self.parler_started:
                self.start_parler()
            self.prompt_ids = self.tokenizer(prompt,return_tensors='pt').input_ids.to(self.device)
            self.generation = self.parler_model.generate(input_ids=self.input_ids, prompt_input_ids=self.prompt_ids)
            audio_arr = self.generation.cpu().numpy().squeeze()
            sf.write(location,audio_arr,self.parler_model.config.sampling_rate)

    def start_playht(self):
        from pyht import Client
        from pyht.client import TTSOptions
        import os
        uid = os.getenv('PLAYHT_USER_ID')
        api_key = os.getenv('PLAYHT_API_KEY')
        client = Client(user_id=uid,api_key=api_key)
        self.pyht_options = TTSOptions(voice=os.getenv('PLAYHT_PALOMA'),sample_rate=44100)
        try:
            result = client.tts('a',self.pyht_options)
            chunks: bytearray = bytearray()
            for chunk in result:
                chunks.extend(chunk)
            result = chunks
            if len(result) > 0:
                return True, client
        except Exception as e:
            print(e, type(e))
            return False, None
            
    def playht_generate(self,prompt,location):
        try:
            audio_arr = self.client.tts(prompt,self.pyht_options)
            save_audio(audio_arr,location)
            return
        except:
            self.fallback(prompt,location)

    def start_parler(self):
        if not self.parler_started:
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
                self.parler_started = True

    def fallback(self,prompt,location):
        if not self.parler_started:
            self.start_parler
        self.parler_generate(prompt,location)

def save_audio(data: Union[Generator[bytes, None, None], Iterable[bytes]], save_location):
    chunks: bytearray = bytearray()
    for chunk in data:
        chunks.extend(chunk)
    with open(save_location, "wb") as f:
        f.write(chunks)



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
    from os import path
    import sys
    import threading

    target_name = ''
    query = ''
    
    load_dotenv()

    tts = tts_manager()
    directory = path.dirname(__file__)
    subdir = path.join(directory,'tones')
    subdir = path.join(subdir,'temporary_sounds')
    
    query = f"Warning! Attempting to login in virtual reality - full sensory override... User may be exposed to biofeedback damage..."
    target_name = 'vr_hot_login'
    filepath = path.join(subdir,f'{target_name}.mp3')
    print(filepath)
    tts.fallback(query.strip(),filepath)
    for thread in threading.enumerate():
        print(thread)