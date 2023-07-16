from Talker import Talker
import subprocess as sp
import os
import time
import iso639

class NAOTalker(Talker):
    def __init__(self, ip: str, language: str = "en", sleep_len: float = 0.03, stand=True):
        self.ip = ip
        self.sleep_len = sleep_len
        fd = os.path.dirname(os.path.realpath(__file__))
        self.talker_path = fd + "/NAOTalkerPy2.py"
        if not os.path.exists(self.talker_path):
            raise RuntimeError(f"NAOTalker can't find 'talker.py' at {self.talker_path}")
        if not os.path.isdir(fd + "/choregrapher"):
            raise RuntimeError(f"NAOTalker can't find Choregrapher at {fd}")
        if not os.path.isdir(fd + "/pynaoqi"):
            raise RuntimeError(f"NAOTalker can't find PyNaoQi at {fd}")
        if not os.path.exists(fd + "/py2_nao_source.sh"):
            f = open(fd + "/py2_nao_source.sh","w")
            f.write(f"export PYTHONPATH=$PYTHONPATH:{fd}/pynaoqi\n")
            f.write(f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{fd}/choregrapher/lib")
            f.close()
        super().__init__(language = language)
        self.language = iso639.Lang(language).name
        if stand: self.nao_say("stand")

    def __del__(self):
        self.nao_say("sit")

    def nao_say(self, to_say):
        for token in ["'",'"']:
            to_say = to_say.replace(token,"")
        sp.run(f"source py2_nao_source.sh ; echo '{to_say}' | python2 {self.talker_path} {self.ip} {self.language}",shell=True, env={},executable='/bin/bash',stdout=sp.DEVNULL)

    def say(self, to_say: str, first: bool = False, last: bool = False):
        """
        Speaks the string to_say

        Args:
            to_say (str): The string to speak
            first (bool): Not used
            last (bool): If NAO should signal when speaking is done via winking
        """
        print(to_say)
        self.nao_say(to_say)
        time.sleep(len(to_say)*self.sleep_len) # As we lack response from the call, wait arbitrary time. This is a decent approximation
        if last:
            self.nao_say('turnoff')
            self.nao_say('turnon')

if __name__ == "__main__":
    from Chatter import Chatter
    from Listener import Listener
    name = "Pepper"
    swe_intro = f"Du är den mänskliga roboten {name}. En NAO-modellrobot byggd av Softbank och programmerad av FIA Robotics. Din uppgift är att hålla en intressant konversation med en grupp människor. Du får max svara med två meningar."
    eng_intro = f"You are the humanoid robot {name}. A NAO model robot built by Softbank and programmed by FIA Robotics. Your task is to hold an interesting conversation with a group of humans. You can at most answer with two sentences"
    chatter = Chatter(eng_intro, stream=True,chat_horison=5,filt_horison=-1)
    listener = Listener(language="en",use_whisper=False) # Change to 'sv' for Swedish
    talker = NAOTalker(ip="192.168.43.234",language="sv",version="V5")
    while(True):
        print(f"Listening")
        heard = listener()
        print(f"Heard: {heard}")
        if heard != "":
            response = chatter(heard)
            talker(response)
