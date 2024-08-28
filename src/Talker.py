from pydub import AudioSegment, playback
from io import BytesIO
from gtts import gTTS

class Talker:
    def __init__(self, language: str = "en"):
        self.language = language

    def __call__(self, to_say: str):
        """
        Speaks the string/string Generator to_say. If it's a generator
        It speaks via stream_say, if string via say

        Args:
            to_say (str): The string to speak
        """
        if isinstance(to_say, str):
            self.say(to_say, first=True, last=True)
        else: # If not a string, it's a string generator
            self.stream_say(to_say)

    def say(self, to_say: str, first: bool = False, last: bool = False):
        """
        Speaks the string to_say

        Args:
            to_say (str): The string to speak
            first (bool): Flag for the first message spoken at once
            last (bool): Flag for the last message spoken at once
        """
    
        raise NotImplementedError
    
    def stream_say(self, to_say: "Generator<str,None,None>"):
        """
        Speaks the string generated by to_say line by line.
        
        Args:
            to_say (str): The string to speak
        """
        res = ""
        first = True
        for mes in to_say:
            res += mes
            while res.count('\n') >= 1:
                pos = res.find('\n')
                self.say(res[0:pos],first=first)
                res = res[pos+1:]
                first = False
        self.say(res,first=first,last=True)
    
class TerminalTalker(Talker):
    def __init__(self, language: str = "en", prefix: str = "\nAssistant: "):
        super().__init__(language=language)
        self.prefix = prefix

    def say(self, to_say: str, first: bool = False, last: bool = False):
        if first: print(self.prefix + to_say)
        else: print(to_say)
        if last: print()

class LocalTalker(Talker):
    def say(self, to_say: str, first: bool = False, last: bool = False):
        try:
            audio = gTTS(to_say,lang=self.language)
            fp = BytesIO()
            audio.write_to_fp(fp)
            fp.seek(0) # Return to start of file
            segment = AudioSegment.from_file(fp,format="mp3")
            playback.play(segment)
        except:
            return

if __name__ == "__main__":
    from Chatter import Chatter
    from Listener import Listener
    name = "Pepper"
    swe_intro = f"Du är den mänskliga roboten {name}. En NAO-modellrobot byggd av Softbank och programmerad av FIA Robotics. Din uppgift är att hålla en intressant konversation med en grupp människor. Du får max svara med två meningar."
    eng_intro = f"You are the humanoid robot {name}. A NAO model robot built by Softbank and programmed by FIA Robotics. Your task is to hold an interesting conversation with a group of humans. You can at most answer with two sentences"
    chatter = Chatter(swe_intro, stream=True,chat_horison=5,filt_horizon=3,name=name)
    listener = Listener("sv",use_whisper=False,default_mic=False) # Change to 'en' for english
    talker = LocalTalker("sv")
    while(True):
        heard = listener()
        print(f"Heard: {heard}")
        if heard != "":
            response = chatter(heard)
            talker(response)
