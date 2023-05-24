from Talker import Talker
import subprocess as sp

class NAOTalker(Talker):
    def __init__(self, ip: str, talker_path: str, language: str = "en"):
        self.ip = ip
        self.talker_path = talker_path
        super().__init__(language = language)

    def say(self, to_say: str):
        """
        Speaks the string to_say

        Args:
            to_say (str): The string to speak
        """
        for token in ["'",'"']:
            to_say = to_say.replace(token,"")
        sp.run(f"source python2_source.sh ; echo '{to_say}' | python2 {self.talker_path} {self.ip}",shell=True, env={},executable='/bin/bash')
        

if __name__ == "__main__":
    from Chatter import Chatter
    from Listener import Listener
    name = "Alice"
    swe_intro = f"Du är den mänskliga roboten {name}. En NAO-modellrobot byggd av Softbank och programmerad av FIA Robotics. Din uppgift är att hålla en intressant konversation med en grupp människor."
    eng_intro = f"You are the humanoid robot {name}. A NAO model robot built by Softbank and programmed by FIA Robotics. Your task is to hold an interesting conversation with a group of humans."
    chatter = Chatter(swe_intro, stream=True,chat_horison=5,filt_horison=3,name=name)
    listener = Listener("sv",use_whisper=False) # Change to 'en' for english
    talker = NAOTalker("10.133.5.209", "~/Documents/NAO_DEMO/nao-demo/V5/python/talker.py","sv")
    while(True):
        heard = "HELLO WORLD"#listener()
        print(f"Heard: {heard}")
        if heard != "":
            response = "HELLO WORLD" #chatter(heard)
            talker(response)
