from Tkinter import *

from naoqi import ALProxy
import time
import threading
import os
import numpy
from random import randint
import random

# from naoqi import ALModule
IP = "192.168.1.3"
PORT = 9559

tts = ALProxy("ALTextToSpeech", IP, PORT)
volume = ALProxy("ALAudioDevice", IP, PORT)
volume.setOutputVolume(50)

behave = ALProxy("ALBehaviorManager", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)

# emotions = []

Anger = ["Let's see. I think it's anger.", "I would say this is anger", "Hmm. Maybe anger?", "I think it's, anger", "This one is hard. Maybe anger?", "Let me think. This is Anger"]
Fear = ["Let's see. I think it's fear.", "I would say this is fear", "Hmm. Maybe fear?", "I think it's, anger", "This one is hard. Maybe fear?"]
Frustration = ["Let's see. I think it's frustration.", "I would say this is frustration", "Hmm. Maybe frustration?", "I think it's, frustration", "This one is hard. Maybe frustration?"]
Happiness = ["Let's see. I think it's happiness.", "I would say this is happiness", "Hmm. Maybe happiness?", "I think it's, happiness", "This one is hard. Maybe happiness?"]
Sadness = ["Let's see. I think it's sadness.", "I would say this is sadness", "Hmm. Maybe sadness?", "I think it's, sadness", "This one is hard. hmm. Maybe sad,ness?"]

emotion = [Anger, Fear, Frustration, Happiness, Sadness]
new_Emotion = [Anger, Fear, Frustration, Happiness, Sadness]  # 2x2array
right_Emotion = []


#loading behaviours into an array
quick_behaviour = ["Sit/BodyTalk/Speaking/BodyTalk_1",
                  "Sit/BodyTalk/Speaking/BodyTalk_2",
                  "Sit/BodyTalk/Speaking/BodyTalk_3",
                  "Sit/BodyTalk/Speaking/BodyTalk_5",
                  "Sit/BodyTalk/Speaking/BodyTalk_6",
                  "Sit/BodyTalk/Speaking/BodyTalk_8",
                  "Sit/BodyTalk/Speaking/BodyTalk_11",
                  "Sit/BodyTalk/Speaking/BodyTalk_12",
                  "Sit/Waiting/ScratchHead_1"]

slower_behavior = [ "Sit/BodyTalk/Speaking/BodyTalk_4",
                    "Sit/BodyTalk/Speaking/BodyTalk_7",
                    "Sit/BodyTalk/Speaking/BodyTalk_9",
                    "Sit/BodyTalk/Speaking/BodyTalk_10"]

#setting the inital count value
count = 0
#saving the initial count value for arduino to access
numpy.savetxt("countB.txt", [count], fmt="%i")
tts.resetSpeed()
tts.setParameter("pitchShift", 1)
#
# checkMark = 0

def markDetection():
    global count

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
    # Check whether we got a valid output: a list with two fields.
        if (val and isinstance(val, list) and len(val) >= 2):
            time.sleep(1.0)
                # For each mark, we can read its shape info and ID.
                # First Field = TimeStamp.
            timeStamp = val[0]
                # Second Field = array of Mark_Info's.
            markInfoArray = val[1]

            try:
                # time.sleep(1.0)

                motion.setAngles("HeadYaw", random.uniform(0, 0), 0.2)
                    # Browse the markInfoArray to get info on each detected mark.
                for markInfo in markInfoArray:

                    nu = numpy.genfromtxt("arduinoB.txt", int)
                    # First Field = Shape info.
                    markShapeInfo = markInfo[0]
                    # Second Field = Extra info (i.e., mark ID).
                    markExtraInfo = markInfo[1]

                    tts.stopAll()
                    # tts = ALProxy("ALTextToSpeech", IP, PORT)
                    time.sleep(.5)

                    tts.setParameter("speed", 50 + (nu * 25))
                    tts.setParameter("pitchShift", 1)

                    #fetching the answer of the user from the saved txt file
                    name = numpy.genfromtxt("UI.txt", str)

                    if int(nu) <= 3:
                        response = random.choice(slower_behavior)
                    elif int(nu) > 3:
                        response = random.choice(quick_behaviour)

                    emotions = ["Anger", "Fear", "Frustration", "Happiness", "Sadness"]
                    new_Emotion = [Anger, Fear, Frustration, Happiness, Sadness]  # 2x2array
                    right_Emotion = []
                   # right_Emotion = [Anger, Fear, Frustration, Happiness, Sadness]

                    #eliminating the emotion the user chooses from the UI
                    for x in range(0, 5):
                        if str(name) == emotions[x]:
                            right_Emotion.append(emotion[x])
                            new_Emotion.remove(new_Emotion[x])


                    #1 emotion - Sadness
                    if markExtraInfo[0] == 64:
                        speech = random.choice(random.choice(new_Emotion))    #incorrect
                        response
                    #2 emotion - Anger
                    elif markExtraInfo[0] == 68:
                        speech = random.choice(random.choice(right_Emotion))
                    #3 emotion - Fear
                    elif markExtraInfo[0] == 80:
                        speech = random.choice(random.choice(new_Emotion))     #incorrect
                    #4 Sadness
                    elif markExtraInfo[0] == 84:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect
                    #5 Frustration
                    elif markExtraInfo[0] == 85:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect
                    #6 Happiness
                    elif markExtraInfo[0] == 107:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect
                    #7 Sadness
                    elif markExtraInfo[0] == 108:
                        speech = random.choice(random.choice(right_Emotion))
                    #8 Anger
                    elif markExtraInfo[0] == 112:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect
                    #9 Fear
                    elif markExtraInfo[0] == 119:
                        speech = random.choice(random.choice(right_Emotion))
                    #10 Happiness
                    elif markExtraInfo[0] == 114:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect
                    #11 Frustration
                    elif markExtraInfo[0] == 170:
                        speech = random.choice(random.choice(right_Emotion))
                    #12 Fear
                    elif markExtraInfo[0] == 130:
                        speech = random.choice(random.choice(right_Emotion))
                    #13 Sadness
                    elif markExtraInfo[0] == 187:
                        speech = random.choice(random.choice(new_Emotion))  # incorrect

                    #speak the answer
                    motion.wakeUp()
                    behave.startBehavior(response)
                    tts.say(speech)
                    # Print Mark information.
                    print val
                    count += 1
                    numpy.savetxt("countB.txt", [count], fmt="%i")
                    os.remove("arduinoB.txt")
                    os.remove("UI.txt")

                    checkMark = markExtraInfo[0]
                    # posture.goToPosture("Sit", 0.5)
                    # time.sleep(3)

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
                    tts.say("Looks like you have not given any feedback from the UI. Please give your feedback and then show me the card.")

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
    # t1 = threading.Thread(target = show_Up_UI)
    t2 = threading.Thread(target = markDetection)

    # t1.start()
    t2.start()

    # t1.join()
    t2.join()

    # main()

def btnClicked(btn):
    print(btn)
    tts.say("I think this is a sad emotion")

if __name__ == "__main__":
    main()



