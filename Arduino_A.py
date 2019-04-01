import serial #importing serial library
import random
from naoqi import ALProxy
import numpy
import os
import time
from pathlib2 import Path
import paramiko


IP = "192.168.1.3"
PORT = 9559

#proxy to text to speech, LED lights and behviour modules
tts = ALProxy("ALTextToSpeech", IP, PORT)
proxy = ALProxy("ALLeds", IP, PORT)
behave = ALProxy("ALBehaviorManager", IP, PORT)

# behave_proxy = ALProxy("ALBehaviorManager")

volume = ALProxy("ALAudioDevice", IP, PORT)
volume.setOutputVolume(50)

motion = ALProxy("ALMotion", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)
awareness = ALProxy("ALBasicAwareness", IP, PORT)

posture.goToPosture("Sit", 0.2)
# motion.rest()

#defining the leds of the face
names1 = ["FaceLed0", "FaceLed2", "FaceLed4", "FaceLed6"]
proxy.createGroup("pair", names1) #creating the group of the leds

good_Feedback = ["Woohoo, I got it", "Woohoo, I got it. Although, it was a bit tricky",  "Yipiee!!. I knew this one. Almost fooled me there.", "Yes. That was pretty easy.", "Woohooo. I am the best"]
bad_Feedback = ["Oh! no. But I know now.", "Awww. That was a bit challenging", "Silly me. I should be doing better than this.", "I should have known that.", "Oh!. I got it wrong", "Oh no. That's a shame", "Oh no. That was not as easy as I thought it would be."]

# "Sit/Emotions/Positive/Happy_1",

positive_response = ["Sit/Emotions/Positive/Happy_2",
                     "Sit/Emotions/Positive/Happy_3",
                     "Sit/Emotions/Positive/Happy_4",
                     "Sit/BodyTalk/Speaking/BodyTalk_3",
                     "Sit/BodyTalk/Thinking/Remember_3",
                     "Sit/BodyTalk/Speaking/BodyTalk_2"]
# "Sit/Waiting/Think_1"
negative_response = ["Sit/Waiting/Think_1",
                     "Sit/Waiting/Relaxation_2",
                     "Sit/Waiting/Bored_1"]

idle_behavior = ["Sit/BodyTalk/Listening/Listening_2",
                 "Sit/BodyTalk/Listening/Listening_3",
                 "Sit/BodyTalk/Listening/Listening_1"]


arduinoSerialData = serial.Serial('com4', 9600)
copyData = "0"

variable = numpy.ones((100,1))*-1
count = 0
x = 1.0
convert = 3    # initial voice speed value

# save a default value of 3 - determines the speed of NAO's voice
numpy.savetxt("arduino.txt", [convert], fmt="%i")

# delete any existing count.txt file before starting the program
# os.remove("count.txt")
# check_count = 0;

a = 0
while True:
    myfile = Path("C:/Users/nawam/PycharmProjects/NAO/Arduino dataA/" + str(a) + ".txt")
    if myfile.is_file():
        a += 1
    else:
        break

while count <= 12:
    proxy.setIntensity("pair", x)
    awareness.stopAwareness()

    if (arduinoSerialData.inWaiting() > 0): #check if any data is coming from the serial
        myData = arduinoSerialData.readline() # readline reads the data from the port as a string

        check_count = numpy.genfromtxt("count.txt", int)
        if check_count > count:
            convert = min(4, int(int(myData) / 20))
            # array that saves the dial value for later
            variable[count] = int(myData)
            #save the value of the dial for this instance as a text file for NAO to access through Experiment_A and B
            numpy.savetxt("arduino.txt", [convert] ,  fmt = "%i")

            print convert
            #stop NAO talking as the initial condition
            # if count == 0:
            #
            #     count +=1
            #     continue
            #deciding on the positive vs negative response
            if (convert > 3):
                speech = random.choice(good_Feedback)
                response = random.choice(positive_response)
                x = 1.0
                proxy.setIntensity("pair", x)
            elif (convert <= 3):
                speech = random.choice(bad_Feedback)
                response = random.choice(negative_response)
                x = 0.0
                proxy.setIntensity("pair", x)

            tts.stopAll()
            # tts = ALProxy("ALTextToSpeech", IP, PORT)
            time.sleep(.5)

            tts.setParameter("speed", 50 + (convert * 25))
            tts.setParameter("pitchShift", 1 + 0.06*convert)

            behave.startBehavior(response)
            tts.say(speech)
            posture.goToPosture("Sit", 0.5)


            numpy.savetxt("C:/Users/nawam/PycharmProjects/NAO/Arduino dataA/" + str(a) + ".txt", variable, fmt="%s")

            count += 1

        else:
            if count == 0:
                tts.say("You have not shown me any cards yet.")



        # time.sleep(2)
        # motion.rest()


#creating new files for each participant

#save the dial values
# a = 0
# while True:
#     myfile = Path("C:/Users/nawam/PycharmProjects/NAO/Arduino data/" + str(a) + ".txt")
#     if myfile.is_file():
#         a += 1
#     else:
numpy.savetxt ("C:/Users/nawam/PycharmProjects/NAO/Arduino dataA/" + str(a) + ".txt", variable , fmt = "%s")
        # break

time.sleep(5.0)
awareness.startAwareness()
behave.startBehavior(positive_response[3])
tts.say("This part of the experiment is now over. Thank you for being a part of this. Please proceed to the next part as given in the description")
time.sleep(2)
behave.startBehavior("Sit/Waiting/Relaxation_3")
tts.say("Meanwhile, I need to get some rest. I feel tired.")

# ssh = paramiko.SSHClient()
# ssh.connect(server, username= nao, password= nao)
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("psql -U factory -d factory -f /tmp/data.sql")


