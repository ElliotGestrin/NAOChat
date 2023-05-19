#import naoqi
import sys

nao_ip = "nao_robot_ip"
nao_port = 9559

"""
try:
    # Create an ALAudioDevice proxy
    audio_proxy = naoqi.ALProxy("ALAudioDevice", nao_ip, nao_port)

    # Set the microphone configuration
    audio_proxy.setClientPreferences("RemoteMic", 16000, naoqi.AL.CHANNEL_FRONT_MIC, 0, 0)


    # Subscribe to microphone audio data
    audio_proxy.subscribe("RemoteMic")

    # Start listening to microphone data
    audio_proxy.startMicrophonesRecording("/path/to/save/recording.wav", "wav", 16000, naoqi.AL.CHANNEL_FRONT_MIC)

except naoqi.ALError as e:
    pass
"""
    
    # Wait for microphone data
        # Retrieve the microphone data
        #microphone_data = audio_proxy.readAudioBuffer("RemoteMic")

counter = 0  

while True:  
    sys.stdout.write("TEEEESTING")
    sys.stdout.flush()
    counter += 1  


print("Loop finished")






