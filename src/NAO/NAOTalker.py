import sys
from os import path
# Append to path to find the "Talker" class in the parent dictionary
sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))
from Talker import Talker
import subprocess as sp
import time
import iso639

class NAOTalker(Talker):
    def __init__(self, ip: str, language: str = "en", sleep_len: float = 0.03, stand=False, volume: int = 100):
        super().__init__(language = language)
        self.ip = ip
        self.sleep_len = sleep_len
        self.language = iso639.Lang(language).name
        self.volume = volume
        self.standing = stand
        fd = path.dirname(path.realpath(__file__))
        root_dir = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))
        self.talker_path = fd + "/NAOTalkerPy2.py"
        self.src_path = fd + "/py2_nao_source.sh"
        if not path.exists(self.talker_path):
            raise RuntimeError(f"NAOTalker can't find 'talker.py' at {self.talker_path}")
        if not path.isdir(root_dir + "/choregrapher"):
            raise RuntimeError(f"NAOTalker can't find Choregrapher at {root_dir}")
        if not path.isdir(root_dir + "/pynaoqi"):
            raise RuntimeError(f"NAOTalker can't find PyNaoQi at {root_dir}")
        if not path.exists(self.src_path):
            f = open(self.src_path,"w")
            f.write(f"export PYTHONPATH=$PYTHONPATH:{root_dir}/pynaoqi\n")
            f.write(f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{root_dir}/choregrapher/lib")
            f.close()
        if stand: self.nao_say("stand")

    def __del__(self):
        if self.standing: self.nao_say("sit")

    def nao_say(self, to_say):
        for token in ["'",'"']:
            to_say = to_say.replace(token,"")
        sp.run(
            f"source {self.src_path} ; echo '{to_say}' | tr -d '\n' | python2 {self.talker_path} {self.ip} {self.language} {self.volume}",
            shell=True, env={},executable='/bin/bash',stdout=sp.DEVNULL
        )

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
        time.sleep(len(to_say.strip())*self.sleep_len) # As we lack response from the call, wait arbitrary time. This is a decent approximation
        if last:
            self.nao_say('turnoff')
            self.nao_say('turnon')
            if self.standing: self.nao_say('e')

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
