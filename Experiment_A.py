from Tkinter import *

from naoqi import ALProxy
import time
import threading
import os
import numpy
from random import randint
import random
import os.path
import logging

# from naoqi import ALModule
IP = "192.168.1.3"
PORT = 9559

#proxy to text to speech module
tts = ALProxy("ALTextToSpeech", IP, PORT)
#proxy to control the volume level
volume = ALProxy("ALAudioDevice", IP, PORT)
volume.setOutputVolume(50)
#proxy to behviour module
behave = ALProxy("ALBehaviorManager", IP, PORT)

motion = ALProxy("ALMotion", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)

#dialogues for giving the answers
anger = ["Let's see. I think it's anger.", "I would say this is anger", "Hmm. Maybe anger?", "I think it's, anger", "This one is hard. Maybe anger?"]
fear = ["Let's see. I think it's fear.", "I would say this is fear", "Hmm. Maybe fear?", "I think it's, anger", "This one is hard. Maybe fear?"]
frustration = ["Let's see. I think it's frustration.", "I would say this is frustration", "Hmm. Maybe frustration?", "I think it's, frustration", "This one is hard. Maybe frustration?"]
happiness = ["Let's see. I think it's happiness.", "I would say this is happiness", "Hmm. Maybe happiness?", "I think it's, happiness", "This one is hard. Maybe happiness?"]
sadness = ["Let's see. I think it's sadness.", "I would say this is sadness", "Hmm. Maybe saadness?", "I think it's, sadness", "This one is hard. Maybe sadness?"]

#loading behaviours into an array
quick_behaviour = ["Sit/BodyTalk/Speaking/BodyTalk_1",
                  "Sit/BodyTalk/Speaking/BodyTalk_2",
                  "Sit/BodyTalk/Speaking/BodyTalk_3",
                  "Sit/BodyTalk/Speaking/BodyTalk_5",
                  "Sit/BodyTalk/Speaking/BodyTalk_6",
                  "Sit/BodyTalk/Speaking/BodyTalk_8",
                  "Sit/BodyTalk/Speaking/BodyTalk_11",
                  "Sit/BodyTalk/Speaking/BodyTalk_12"]

slower_behavior = [ "Sit/BodyTalk/Speaking/BodyTalk_4",
                    "Sit/BodyTalk/Speaking/BodyTalk_7",
                    "Sit/BodyTalk/Speaking/BodyTalk_9",
                    "Sit/BodyTalk/Speaking/BodyTalk_10"]

think_response = ["Sit/Waiting/Think_3",
                  "Sit/Waiting/Think_2",
                  "Sit/Waiting/Think_1"]


#setting the inital count value
count = 0
#saving the initial count value for arduino to access
numpy.savetxt("count.txt", [count], fmt="%i")


tts.resetSpeed()
tts.setParameter("pitchShift", 1)

# checkMark = 0

def markDetection():
    global count

    # tts.setVoice("Kenny22Enhanced")

    try:
        landMarkProxy = ALProxy("ALLandMarkDetection", IP, PORT)
    except Exception, e:
        print "Error when creating landmark detection proxy:"
        print str(e)
        exit(1)

    # Subscribe to the ALLandMarkDetection proxy
    # This means that the module will write in ALMemory with
    # the given period below
    period = 500
    landMarkProxy.subscribe("Test_LandMark", period, 0.0)

    memValue = "LandmarkDetected"

    # Create a proxy to ALMemory
    try:
        memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception, e:
        print "Error when creating memory proxy:"
        print str(e)
        exit(1)

    print "Creating landmark detection proxy"

    # A simple loop that reads the memValue and checks whether the symbols are detected.
    while count <= 12:
        time.sleep(0.05)

        val = memoryProxy.getData(memValue)
        print "\*****"
        print(time.time())
    # Check whether we got a valid output: a list with two fields.
        if (val and isinstance(val, list) and len(val) >= 2):

            motion.setAngles("HeadYaw", random.uniform(0, 0), 0.05)
            # time.sleep(1.0)
                # For each mark, we can read its shape info and ID.
                # First Field = TimeStamp.
            timeStamp = val[0]
                # Second Field = array of Mark_Info's.
            markInfoArray = val[1]



            try:
                # time.sleep(1.0)
                # Browse the markInfoArray to get info on each detected mark.
                for markInfo in markInfoArray:

                        # First Field = Shape info.
                    markShapeInfo = markInfo[0]
                        # Second Field = Extra info (i.e., mark ID).
                    markExtraInfo = markInfo[1]

                    nu = numpy.genfromtxt("arduino.txt", int)

                     # if count == 0:
                    #     tts.setParameter("speed", 100)
                    #     tts.setParameter("pitchShift", 1)
                    # else:
                    tts.stopAll()
                    # tts = ALProxy("ALTextToSpeech", IP, PORT)
                    time.sleep(.5)

                    tts.setParameter("speed", 50 + (nu * 25))
                    tts.setParameter("pitchShift", 1)

                    if int(nu) <= 3:
                        response = random.choice(slower_behavior)
                    elif int(nu) > 3:
                        response = random.choice(quick_behaviour)


                    #1 emotion - Sadness
                    if markExtraInfo[0] == 64:
                        speech = random.choice(frustration) #incorrect answer
                    #2 emotion - Anger
                    elif markExtraInfo[0] == 68:
                        speech = random.choice(anger)
                    #3 emotion - Fear
                    elif markExtraInfo[0] == 80:
                        speech = random.choice(frustration)#incorrect
                    #4 Sadness
                    elif markExtraInfo[0] == 84:
                        speech = random.choice(fear)#incorrect
                    #5 Frustration
                    elif markExtraInfo[0] == 85:
                        speech = random.choice(sadness)#incorrect
                    #6 Happiness
                    elif markExtraInfo[0] == 107:
                        speech = random.choice(fear)#incorrect
                    #7 Sadness
                    elif markExtraInfo[0] == 108:
                        speech = random.choice(sadness)
                    #8 Anger
                    elif markExtraInfo[0] == 112:
                        speech = random.choice(sadness)#incorrect
                    #9 Fear
                    elif markExtraInfo[0] == 119:
                        speech = random.choice(fear)
                    #10 Happiness
                    elif markExtraInfo[0] == 114:
                        speech = random.choice(frustration)  # incorrect
                    #11 Frustration
                    elif markExtraInfo[0] == 170:
                        speech = random.choice(frustration)
                    #12 Fear
                    elif markExtraInfo[0] == 130:
                        speech = random.choice(fear)
                    #13 Sadness
                    elif markExtraInfo[0] == 187:
                        speech = random.choice(anger)#incorrect

                    motion.wakeUp()
                    behave.startBehavior(response)


                    #speak the answer
                    tts.say(speech)
                    # Print Mark information.
                    print val
                    count += 1
                    numpy.savetxt("count.txt", [count], fmt="%i")

                    os.remove("arduino.txt")

                    checkMark =  markExtraInfo[0]


                    # posture.goToPosture("Sit", 0.5)
                    # time.sleep(3)
                    # motion.rest()


                    # tts.say("The mark ID is. " markExtraInfo[0])
                    # print "mark  ID: %d" % (markExtraInfo[0])
                    # print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                    # print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])
            except Exception, e:
                tts.stopAll()
                # tts = ALProxy("ALTextToSpeech", IP, PORT)
                time.sleep(.5)

                try:
                    if checkMark != markExtraInfo[0]:
                        tts.say("Looks like you have not given me any feedback. Please give your feedback and then show me the card.")
                    else:
                        print "Landmarks detected, but it seems getData is invalid. ALValue ="
                        print val
                        print "Error msg %s" % (str(e))
                except:
                    tts.say(
                        "Looks like you have not given any feedback from the UI. Please give your feedback and then show me the card.")

        else:
            print("not seen")
            rand = randint(0, 99)
            if rand > 96:
                motion.setAngles("HeadYaw", random.uniform(-0.6, 0.6), random.uniform(0.03, 0.1))
            elif rand > 94:
                motion.setAngles("HeadPitch", random.uniform(-0.2, 0.2), random.uniform(0.03, 0.1))


            # tts.say(" I am sorry. I cannot see the image. Please put it at a distance of  around 30 centimeters from my eyes. Thank you ")

        # nu = numpy.genfromtxt("arduino.txt", int)
        # if nu

    # Unsubscribe from the module.
    landMarkProxy.unsubscribe("Test_LandMark")
    print "Test terminated successfully."


def main():
    markDetection()


if __name__ == "__main__":
    main()



