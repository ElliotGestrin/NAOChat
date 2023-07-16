#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is adapted from the Nao-Demo repo: https://gitlab.liu.se/frelo91/nao-demo
import sys
from naoqi import ALProxy
import random
import cmd
import time
import readline
import rlcompleter
import atexit
import os

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


historyPath = os.path.expanduser("~/.talkerhistory")

def save_history(historyPath=historyPath):
    readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)

class Talker(cmd.Cmd, object):
    """ Simple interactive talk program """

    def __init__(self, robot, language="English"):
        #super(Talker, self).__init__()
        cmd.Cmd.__init__(self)

        try:
            self._posture =  ALProxy("ALRobotPosture", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALPosture for "+robot)
            print(e.message)
            exit(0)
        try:
            self._tts = ALProxy("ALTextToSpeech", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALTextToSpeech for " + robot)
            print(e.message)
            exit(0)
        try:
            self._talk = ALProxy("ALAnimatedSpeech", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALAnimatedSpeech for " + robot)
            print(e.message)
            exit(0)
        try:
            self._audio = ALProxy("ALAudioDevice", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALAudioDevice for " + robot)
            print(e.message)
            exit(0)
        try:
            self._motion = ALProxy("ALMotion", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALMotion for " + robot)
            print(e.message)
            exit(0)
        try:
            self._behavior = ALProxy("ALBehaviorManager", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALBehaviorManager")
            print(e.message)
            exit(0)
        try:
            self._leds = ALProxy("ALLeds", robot, 9559)
        except Exception, e:
            print("Error creating proxy to ALLeds")
            print(e.message)
            exit(0)


            
        
        if language in self._tts.getAvailableLanguages():
            self._tts.setLanguage(language)
        else:
            self._tts.setLanguage("English")
        self._audio.setOutputVolume(20)

        self._modifier = "\RSPD=75\ "
        self._index = 0

        self._talk.declareTagForAnimations({
            "vacuum": ["animations/Stand/Waiting/Vacuum_1"],
            "drivecar": ["animations/Stand/Waiting/DriveCar_1"],
            "headbang": ["animations/Stand/Waiting/Headbang_1"],
            "heat": ["animations/Stand/Reactions/Heat"],
            "lightshine": ["animations/Stand/Reactions/LightShine"],
            "seesomething": ["animations/Stand/Reactions/SeeSomething"],
            "shakebody": ["animations/Stand/Reactions/ShakeBody"],
            "touchhead": ["animations/Stand/Reactions/TouchHead"],
            "airjuggle": ["animations/Stand/Waiting/AirJuggle"],
            "backrubs": ["animations/Stand/Waiting/BackRubs"],
            "bandmaster": ["animations/Stand/Waiting/Bandmaster"],
            "binoculars": ["animations/Stand/Waiting/Binoculars"],
            "callsomeone": ["animations/Stand/Waiting/CallSomeone"],
            "drink": ["animations/Stand/Waiting/Drink"],
            "fitness": ["animations/Stand/Waiting/Fitness"],
            "happybirthday": ["animations/Stand/Waiting/HappyBirthday_1"],
            "helicopter": ["animations/Stand/Waiting/Helicopter"],
            "hideeyes": ["animations/Stand/Waiting/HideEyes"],
            "spaceshuttle": ["animations/Stand/Waiting/SpaceShuttle_1"],
            "airguitar": ["animations/Stand/Waiting/AirGuitar_1"],
            "applause": ["animations/Gestures/Applause_1"],
            "laugh": ["animations/Emotions/Positive/Laugh_1", "animations/Emotions/Positive/Laugh_2", "animations/Emotions/Positive/Laugh_3"],
            "sneeze": ["animations/Emotions/Neutral/Sneeze"]
        })

        names = self.get_names()
        self._commands = []
        for name in names: 
            if name[:3] == 'do_':
                self._commands.append(name[3:])

        print(self._commands)


    def do_talk(self, line):
        self.do_t(line)
    def help_talk(self):
        self.help_t()
    def do_t(self, line):
        if(WALKING):
            self._tts.post.say(self._lines[self._index])
        else:
            self._talk.post.say(self._modifier + self._lines[self._index])
        self._index += 1
        if self._index > len(self._lines)-1:
            self._index = 0
    def help_t(self):
        print("Says something random")

    def do_yes(self, line):
        self.do_y(line)
    def help_yes(self):
        self.help_y()
    def do_y(self, line): # Yes_1, Yes_2, Yes_3
        self._talk.post.say(self._modifier + "^startTag(yes) " + str(line) + " ^waitTag(yes)")
    def help_y(self):
        print("Show yes / positive animation")

    def do_no(self, line):
        self.do_n(line)
    def help_no(self):
        self.help_n()
    def do_n(self, line): # No_3, No_8, No_9
        self._talk.post.say(self._modifier + "^startTag(no) " + str(line) + " ^waitTag(no)")
    def help_n(self):
        print("Show no / negative animation")

    def do_without(self, line):
        self.do_w(line)
    def help_without(self):
        self.help_w()
    def do_w(self, line):
        self._talk.post.say(self._modifier + "^mode(disabled) " + str(line) + " ^mode(contextual)")
    def help_w(self):
        print("Talk without animation")

    def do_happy(self, line):
        self.do_h(line)
    def help_happy(self):
        self.help_h()
    def do_h(self, line): # Enthusiastic_4, Enthusiastic_5
        self._talk.post.say(self._modifier + "^startTag(happy) " + str(line) + " ^waitTag(happy)")
    def help_h(self):
        print("Happy / Enthusiastic")

    def do_birthday(self, line): # Enthusiastic_4, Enthusiastic_5
        self._talk.post.say(self._modifier + "^startTag(happybirthday) " + str(line) + " ^waitTag(happybirthday)")
    def help_birthday(self):
        print("Sings happy birthday")

    def do_vacuum(self, line):
        self._talk.post.say(self._modifier + "^startTag(vacuum)" + str(line) + " ^waitTag(vacuum)")
    def help_vacuum(self):
        print("Vacuum")

    def do_drivecar(self, line):
        self._talk.post.say(self._modifier + "^startTag(drivecar)" + str(line) + " ^waitTag(drivecar)")
    def help_drivecar(self):
        print("Drivecar")

    def do_headbang(self, line):
        self._talk.post.say(self._modifier + "^startTag(headbang)" + str(line) + " ^waitTag(headbang)")
    def help_headbang(self):
        print("Headbang")

    def do_heat(self, line):
        self._talk.post.say(self._modifier + "^startTag(headbang)" + str(line) + " ^waitTag(headbang)")
    def do_headbang(self, line):
        self._talk.post.say(self._modifier + "^startTag(headbang)" + str(line) + " ^waitTag(headbang)")


    def do_spaceshuttle(self, line):
        self._talk.post.say(self._modifier + "^startTag(spaceshuttle)" + str(line) + " ^waitTag(spaceshuttle)")
    def help_spaceshuttle(self):
        print("Spaceshuttle")

    def do_airguitar(self, line):
        self._talk.post.say(self._modifier + "^startTag(airguitar)" + str(line) + " ^waitTag(airguitar)")
    def help_airguitar(self):
        print("Airguitar")

    def do_applause(self, line):
        self._talk.post.say(self._modifier + "^startTag(applause)" + str(line) + " ^waitTag(applause)")
    def help_applause(self):
        print("Applause")

    def do_laugh(self, line):
        self._talk.post.say(self._modifier + "^startTag(laugh)" + str(line) + " ^waitTag(laugh)")
    def help_laugh(self):
        print("Laugh")

    def do_sneeze(self, line):
        self._talk.post.say(self._modifier + "^startTag(sneeze)" + str(line) + " ^waitTag(sneeze)")
    def help_sneeze(self):
        print("Sneeze")


    def do_please(self, line):
        self.do_p(line)
    def help_please(self):
        self.help_p()
    def do_p(self, line): # Please_1
        self._talk.post.say(self._modifier + "^startTag(please) " + str(line) + " ^waitTag(please)")
    def help_p(self):
        print("Please animation")

    def do_unknown(self, line):
        self.do_u(line)
    def help_unknown(self):
        self.help_u()
    def do_u(self, line): # IDontKnow_1, IDontKnow_2
        self._talk.post.say(self._modifier + "^startTag(undetermined) " + str(line) + " ^waitTag(undetermined)")
    def help_u(self):
        print("I dont know animation")

    def do_explain(self, line):
        self.do_e(line)
    def help_explain(self):
        self.help_e()
    def do_e(self, line):
        self._talk.post.say(self._modifier + "^startTag(explain) " + str(line) + " ^waitTag(explain)")
    def help_e(self):
        print("Explain animation")



    def do_intro(self, line):
        self._talk.say(self._modifier + "^startTag(hi) Hej hej! ^waitTag(hi)")
        time.sleep(0.7)
        self._talk.say(self._modifier + "^startTag(explain) Jag är en liten råbott ^waitTag(explain)")
        self._talk.say(self._modifier + "^startTag(undetermined) Skulle vi inte få träffa fredrik, kanske ni tänker? ^waitTag(undetermined)")
        time.sleep(0.8)
        self._talk.say(self._modifier + "^startTag(explain) Jag kollade upp tåg tider på Internet. ^waitTag(explain)")
        time.sleep(1)
        self._talk.say(self._modifier + "^startTag(explain) och han skulle inte hinna till er nu på morgonen. ^waitTag(explain)")
        time.sleep(0.8)
        self._talk.say(self._modifier + "^startTag(me) Låt mig presentera Fredrik Löfgren via länk!  ^waitTag(me)")


    def do_bow(self, line): #BowShort_1
        self._talk.post.say(self._modifier + "^startTag(bow) " + str(line) + " ^waitTag(bow)")
    def help_bow(self):
        print("Bow animation")

    def do_hi(self, line): # Hey_1, Hey_6
        self._talk.post.say(self._modifier + "^startTag(hello) " + str(line) + " ^waitTag(hello)")
    def help_hi(self):
        print("Hello, hi, hey animation")

    def do_me(self, line): #Me_1, Me_2
        self._talk.post.say(self._modifier + "^startTag(me) " + str(line) + " ^waitTag(me)")
    def help_me(self):
        print("Myself, me, I animation")

    def do_you(self, line): #You_1. You_4
        self._talk.post.say(self._modifier + "^startTag(you) " + str(line) + " ^waitTag(you)")
    def help_you(self):
        print("You, Your animation")

    def do_gangnam(self, line):
        self._behavior.post.runBehavior("gangnam-6e6cc7/gangnam")
    def do_penny(self, line):
        self._behavior.runBehavior("tjejerrbst-e0ebff/behavior_1")
    def do_thriller(self, line):
        self._behavior.post.runBehavior("thriller-329b54/behavior_1")
    def do_lullaby(self, line):
        self._behavior.post.runBehavior("lullaby-9f5c56/lullaby")
    def do_macarena(self, line):
        self._behavior.post.runBehavior("robotappstore_naodancesthemacarena-2bcf62/RobotAppStore_NAO Dances The Macarena")
    def do_jingle(self, line):
        self._behavior.post.runBehavior("jingle_bell_rock-2fc93f/jingle_bell_rock")
    def do_sitgive(self, line):
        self._behavior.post.runBehavior("sit-give-276854/behavior_1")
    def do_sithold(self, line):
        self._behavior.post.runBehavior("sit-hold-9b2d21/behavior_1")
    def do_sing(self, line):
        self.do_jingle(line)
    def do_dance(self, line):
        self.do_gangnam(line)
    def do_stop(self, line):
        self._behavior.stopAllBehaviors()

        

        
    def do_exit(self, line):
        self._posture.goToPosture("Sit",0.8)
        self._motion.setStiffnesses("Body", 0.0)
        exit()
    def help_exit(self):
        print("Exit the program")

    def do_sit(self, line):
        self._posture.goToPosture("Sit",0.8)
        self._motion.setStiffnesses("Body", 0.0)
    def help_sit(self):
        print("Sit down animation")

    def do_stand(self, line):
        self._posture.goToPosture("Stand",0.8)
    def help_stand(self):
        print("Stands up animation")

    def do_turnon(self, line):
        self._leds.on("AllLeds")

    def do_turnoff(self, line):
        self._leds.off("AllLeds")
        
        
    def do_walkf(self, line):
	    self._motion.walkTo(1,0,0)

    def do_EOF(self, line):
        return True
        
    def default(self, line):
        if (WALKING):
            self.do_without(line)
        else:
            self._talk.post.say(self._modifier + str(line))

    def emptyline(self):
        if not DEFAULT_QUIET:
            super(Talker, self).emptyline()



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage python talker.py ROBOT_IP")
    else:
        global WALKING
        global DEFAULT_QUIET
        ip = sys.argv[1]
        if len(sys.argv) >= 2: language = sys.argv[2]
        WALKING = "walking" in sys.argv
        DEFAULT_QUIET = "quiet" in sys.argv
        
        Talker(ip, language).cmdloop()
