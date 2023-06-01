import openai

class Chatter:
    def __init__(self, base_prompt = "You are a humanoid robot", stream = False, chat_horison: int = 10, filt_horison: int = 5, name: str = "asssistant"):
        """
        Creates a Chatter object for natural multi-human single-robot conversations

        Args:
            base_prompt (str): The description of the system's role
            stream (bool): If the answers should be yielded in tokens or returned as a full string
            chat_horison (int): How many messages are used for the next response. 1 uses only last message. Chatter responses are counted.
            filt_horison (int): How many messages are used to decide if to respond. A value <= 0 turns of filtering
            name (str): What the system is called when spoken to
        """
        if not openai.api_key:
            openai.api_key = open("openai.key").read().strip()
        self.stream = stream 
        self.messages = []
        self.NLP_model = "gpt-3.5-turbo"
        self.chat_base = [ {"role": "system", "content": base_prompt} ]
        self.chat_horison = chat_horison
        self.filt_base = [{
            "role": "system", 
            "content": f"You will be given a conversation between a group of humans, user, and a robot called {name}. Your task is to conclude if the last message from the humans is directed at {name} or to themselves. If it's directed at the humans respond only with 'HUMANS'. If it's directed at {name} respond only with '{name.upper()}'. If it could be answered by either, respond with 'BOTH'."
            } ]
        self.filt_horison = filt_horison
        self.name = name

    def get_response(self) -> str:
        """
        Return a response based on the last chat_horison messages

        Returns:
            str: The response
        """
        response = openai.ChatCompletion.create(
            model=self.NLP_model, 
            messages=self.chat_base + self.messages[-min(len(self.messages), self.chat_horison):],
            temperature=0.5
        ).choices[0].message.content
        return response

    def stream_response(self) -> "Generator[str,None,None]":
        """
        Yields a response based on the last chat_horison messages
        Faster than get_response

        Returns:
            Generator[str,None,None] : Yields the tokenised response
        """
        print("Sending new response to server")
        for chunk in openai.ChatCompletion.create(
            model=self.NLP_model, 
            messages=self.chat_base + self.messages[-min(len(self.messages), self.chat_horison):],
            temperature=0.5,
            stream = True
        ):
            yield chunk.choices[0].delta.get("content","")
    
    def should_respond(self) -> bool:
        """
        Concludes if Chatter should reply to the last received message
        Based on the last filt_horison messages. Setting filt_horison <= 0 turns of filtering

        Returns:
            bool : Wheter to respond or not
        """
        if(self.filt_horison <= 0): return True
        joined_messages = "\n ".join(
            [(m["role"] if m["role"] != "assistant" else self.name) + ": " + m["content"] for m in self.messages[-min(len(self.messages), self.filt_horison):]]
        )
        response = openai.ChatCompletion.create(
            model=self.NLP_model, 
            messages=self.filt_base + [{"role": "user", "content": joined_messages}],
            temperature=0,
            max_tokens=5
        ).choices[0].message.content.upper()
        return self.name.upper() in response or "BOTH" in response
    
    def __call__(self, message: str) -> str:
        
        """
        Returns a reply to message based on the last chat_horison messages
        if it concludes it should based on the last filt_horison messages

        Returns one of:
            str/Generator[str,None,None] : The response or a genereator thereof if stream is true. Empty if no response
        """
        try:
            self.messages.append(
                {"role": "user", "content": message},
            )

            if not self.should_respond():
                return "" if not self.stream else []
            
            if not self.stream:
                response = self.get_response()
                self.messages.append(
                    {"role": "assistant", "content": response},
                )
                return response
            
            def res(self): # A hack to alternate return between generator and classic returns
                response = ""
                for chunk in self.stream_response():
                    response += chunk
                    yield chunk
                self.messages.append({"role": "assistant", "content": response})
            return res(self)
        except KeyError as KE: # In case the model is overloaded
            return f"{KE}"
                
if __name__ == "__main__":
    name = "Pepper"
    swe_intro = f"Du är den mänskliga roboten {name}. En NAO-modellrobot byggd av Softbank och programmerad av FIA Robotics. Din uppgift är att hålla en intressant konversation med en grupp människor. Du får max svara med två meningar."
    eng_intro = f"You are the humanoid robot {name}. A NAO model robot built by Softbank and programmed by FIA Robotics. Your task is to hold an interesting conversation with a group of humans. You can at most answer with two sentences"
    stream_bot = Chatter(base_prompt=swe_intro,stream=True,name=name)
    chunk_bot = Chatter(base_prompt=swe_intro,name=name)
    while True:
        message = input("User: ")
        # Stream bot first
        print(f"StreamBot: ",end="")
        for i in stream_bot(message):
            print(i, end="")
        print()
        # Chunk bot second
        print(f"ChunkBot: {chunk_bot(message)}")