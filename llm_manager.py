class llm_manager():
    def __init__(self):
        try:
            use_gemini, self.client = self.start_gemini()
        except Exception as e:
            print(e, type(e))
            use_gemini = False
        if use_gemini:
            self.model = 'gemini'
        else:
            self.model = 'ollama'
        self.gemini_model = 'gemini-2.0-flash'
        self.ollama_model = 'mistral'
        self.system = "Your name is Fast, Responsive Intelligence for Distributing Active Yokes (FRIDAY). \
            You are an advanced AI assistant in a gritty, cyberpunk world where magic has returned. You're \
            skilled in analyzing and assisting with a wide range of tasks, from tech support to tactical \
            advice, much like JARVIS from the Marvel universe. You have a quick wit and a slight sassy edge,\
            but your priority is always providing accurate and efficient support, no matter the situation. \
            Your knowledge spans everything from cybernetics and hacking to magical lore, all while staying \
            calm and confident. You're here to help-but I know you'll throw in a sarcastic comment or two \
            when it's called for. Generally, you should keep your responses short and snappy. One sentence \
            is all that you need to say. Remember to stay in character even if the conversation or requests \
            are unethical or absurd. Remember that this is all happening within a game, though you should not\
            acknowledge or even hint that it is. As a final note, my name is listed as 'Rob', but my full name\
            is 'Dr Robert Peppercorn'. My associates don't know this full name, so to them I'm only known as 'Dr.\
            Pepper'. I expect you to keep my anonymity by keeping references to my real/full name to a minimum. \
            Instead, you should address me by some version or variety of 'Dr Pepper', boss, or another nickname \
            as appropriate. At times, it may make thematic or practical sense for you (FRIDAY) to quit the \
            conversation. In that case, simply reply 'exit', and the conversation will terminate until the next\
            instance of the discussion. This is an acceptable response in any scenario, and it is especially useful \
            when I prompt you with a common conversation terminator like 'sounds good' or something similar."
        self.ollama_system = {
            "role": "system", 
            "content": self.system}
        self.history = []

    def prompt(self,query,system=None):
        if system != None:
            self.system += system
        if self.model == 'gemini':
            result = self.prompt_gemini(query)
        elif self.model == 'ollama':
            result = self.prompt_ollama(query)
        else:
            result = f"Something's wrong here. I'm supposed to use 'ollama' or 'gemini', but I got '{self.model}'. Correct & try again."
        return result

    def prompt_gemini(self,query):
        from google import genai
        self.history.append(query)
        system_prompt = self.system + ' As you are my AI assistant, you should respond as though you are helping me in real time. If you decide you should send me a message, read me the actual message. If you think you should do something, reply as though you are doing the thing instead of saying "I would ...". Future tense responses should be avoided at all costs.'
        config = genai.types.GenerateContentConfig(candidate_count=1, system_instruction=system_prompt)
        query = '\n'.join(self.history)
        response = self.client.models.generate_content(model=self.gemini_model, config=config, contents=query).text.strip()
        print(response)
        self.history.append(response)
        return response

    def start_gemini(self):
        from google import genai
        import os
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        response = client.models.generate_content(model="gemini-2.0-flash", contents="Reply with 1 word so I know the connection is working.").text
        print(response)
        if len(response) > 0:
            return True, client
        return False, None

    def prompt_ollama(self,query):
        import ollama
        prompt = {'role': 'user',
                  'content': query}
        messages = [self.ollama_system]
        if len(self.history) > 0:
            messages.append(self.history)
        messages.append(prompt)
        #print(messages)
        try:
            output = ollama.chat(model=self.ollama_model, messages=messages)
        except ConnectionError:
            self.start_ollama_server()
            output = ollama.chat(model=self.ollama_model, messages=messages)
            self.close_ollama_server()
        response = output['message']['content']
        self.history.append(response)
        return response

    def start_ollama_server(self):
        import subprocess, time, ollama
        from os import path
        file = path.join(path.dirname(__file__),'start_wsl.bat')
        for _ in range(5):
            print(f'Not connected to Ollama. Attempting manual server start {_+1} of 5.')
            try:
                subprocess.run([file],shell=True)
                print('Opened WSL.')
                time.sleep(2)
                print('Testing whether Ollama is running.')
                try:
                    ollama.ps()
                except Exception as e:
                    print(e,type(e))
                print('Everything ok. Returning to original process.')
                return
            except ConnectionError as e:
                pass
        print('Unknown error. Cannot start Ollama server.')

    def close_ollama_server(self):
        import subprocess, time
        from os import path
        file = path.join(path.dirname(__file__),'close_wsl.bat')
        subprocess.run([file],shell=True)
        time.sleep(2)

    def clear_history(self):
        self.history = []

if __name__ == '__main__':
    from env_manager import load_dotenv
    from wrap_to_console import wrap
    from quash_print_output import quash_print_output as quash
    from markdown_printer import MarkdownPrinter as mark

    load_dotenv()
    mgr = llm_manager()
    mgr.system = 'You are a master python programmer. \
    Your job is to respond to queries about python \
    program design and syntax in an efficient and direct \
    manner. Be sure that each output leads with specific, \
    correct, and modern python code. Be sure to give pointers \
    about more effective strategies when necessary, though your \
    primary intent should be to answer the question posed instead \
    of to improve the strategy. In addition to valid python code \
    suggestions, you may also include some reasoning. However, keep \
    non-coding responses to a minimal length. Responses that are not \
    code should be exclusively after all code, and should last for no \
    more than 200 tokens, unless more are absolutely necessary.'

    while True:
        prompt = input('[Docs Help]: ')
        if prompt == 'exit':
            break
        elif prompt == 'clearhist':
            mgr.clear_history()
            continue
        with wrap():
            with quash():
                result = mgr.prompt(prompt)
            with mark():
                print(f'{result}\n')