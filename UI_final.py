from Tkinter import *
import tkFont

#from naoqi import ALProxy
import time
import threading
import numpy as np
#from pathlib2 import Path

#variable to track the number of questions = 13
count = 0;

names = np.chararray((20, 2))

#declaring buttons
button1 = Button
button2 = Button
button3 = Button
button4 = Button
button5 = Button    #Next button
button6 = Button
root = Tk()



# 13 texts for button 1
txt1 = ["Sadness",     "Anger",        "Happiness",    "Happiness",     "Sadness",      "Fear",         "Happiness",    "Happiness",    "Anger",        "Sadness",      "Fear",         "Sadness",      "Happiness",    "Sadness"]
# button 2, 3, 4 and 5
txt2 = ["Anger",       "Fear",         "Frustration",  "Frustration",   "Frustration",  "Happiness",    "Frustration",  "Anger",        "Fear",         "Fear" ,        "Frustration",  "Fear",         "Sadness",      "Fear"]
txt3 = ["Happiness",   "Frustration",  "Sadness",      "Fear",          "Happiness",    "Sadness",      "Fear",         "Sadness",      "Happiness",    "Frustration",  "Sadness",      "Happiness",    "Anger",        "Anger"]
txt4 = ["Frustration", "Sadness",      "Fear",         "Sadness",       "Fear",         "Frustration",  "Sadness",      "Frustration",  "Sadness",      "Happiness",    "Anger",        "Anger",        "Frustration",  "Happiness"]
txt5 = ["Fear",        "Happiness",    "Anger",        "Anger",         "Anger",        "Anger",        "Anger",        "Fear",         "Frustration",  "Anger",        "Happiness",    "Frustration",  "Fear",         "Frustration"]

#global variable for changing texts in buttons
a = 0
# array to save participants answers
names1 = []

b = 0
while True:
    #myfile = Path("C:/Users/nawam/PycharmProjects/NAO/User Interface data/" + str(b) + ".txt")
    #if myfile.is_file():
    #    b += 1
    #else:
    #    break

#function to change pages - changes text of the buttons
def changePage():
    global a, root, txt1, txt2, txt3, txt4, button1, button2, button3, button4, button5, names1, theLabel4, count

    nu = np.genfromtxt("arduinoB_checkCount.txt", int)

    if nu > count:

        count += 1
        if a <= 11:
            helv3 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)
            theLabel5 = Label(root,
                              text="                               Choose your Answer                                                      ",
                              font=helv3)
            theLabel5.pack()
            theLabel5.place(x=530, y=500)
            a = a + 1

            np.savetxt("C:/Users/nawam/PycharmProjects/NAO/User Interface data/" + str(b) + ".txt", names1, fmt= "%s")


            #display the question number at the top
            theLabel2 = Label(root, text="Question " + str(a+1))
            theLabel2.pack()
            theLabel2.place(x=680)

            button1.configure(text=txt1[a], state = 'active')
            button2.configure(text=txt2[a], state = 'active')
            button3.configure(text=txt3[a], state = 'active')
            button4.configure(text=txt4[a], state = 'active')
            button6.configure(text=txt5[a], state= 'active')
            button5.configure(state='disabled', background="#808080")

            # display the answer chosen at the bottom
            theLabel3 = Label(root, text="You answer is: " + "                       ")
            theLabel3.pack()
            theLabel3.place(x=650, y=600)


        elif a == 12:
            a += 1
            helv36 = tkFont.Font(family='Helvetica', size=30, weight=tkFont.BOLD)
            theLabel = Label(root, text="End of this part. Please continue with the tablet now.", font = helv36)
            theLabel.pack()
            theLabel.place(x=200, y=260)

            np.savetxt("C:/Users/nawam/PycharmProjects/NAO/User Interface data/" + str(b) + ".txt", names1, fmt="%s")

        else:
            sys.exit()
        return


    else:
        helv2 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)
        theLabel6 = Label(root,
                          text="                               Please give feedback from the dial                                                      ", font=helv2)
        theLabel6.pack()
        theLabel6.place(x=530, y=500)

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

# displaying the UI
def show_Up_UI():
    global a, root, text, button_loop,  txt1, txt2, txt3, txt4, button1, button2, button3, button4, button6
    root.title("HITLabNZ Experiment")
    # FullScreenApp(root)
    # root.minsize(width=1280, height=800)

    # root.maxsize(width=1000, height=350)

    # helv36 = tkFont.Font(family='Helvetica', size=30, weight=tkFont.BOLD)

    # theLabel = Label(root, text="Your Answer is")
    # theLabel.pack()
    # theLabel.place(x=590, y=50)

    #Creating the label for the first page instance
    theLabel2 = Label(root, text="Question 1")
    theLabel2.pack()
    theLabel2.place(x=680)

    helv36 = tkFont.Font(family='Helvetica', size=20, weight = tkFont.BOLD)

    # creating four buttons with text as the variable
    button1 = Button(root, text=txt1[a], height = 3, width = 18, font = helv36, command=lambda: button_function(txt1[a]))
    button1.pack()  # creates the button
    button1.place(x = 200, y= 100)
    button2 = Button(root,  text=txt2[a], height = 3, width = 18, font = helv36, command=lambda: button_function(txt2[a]))
    button2.pack()
    button2.place(x = 850, y = 100)
    button3 = Button(root, text=txt3[a], height = 3, width = 18, font = helv36, command=lambda: button_function(txt3[a]))
    button3.pack()
    button3.place(x = 200, y = 300)
    button4 = Button(root,  text=txt4[a], height = 3, width = 18, font = helv36, command=lambda: button_function(txt4[a]))
    button4.pack()
    button4.place(x = 850, y = 300)
    button6 = Button(root, text=txt5[a], height=3, width=18, font=helv36, command=lambda: button_function(txt5[a]))
    button6.pack()
    button6.place(x=525, y=200)

    # button5 = Button(root, text="Next", command=changePage)
    # button5.pack()
    # button5.place(x=150, y=200)
    app = FullScreenApp(root)
    root.mainloop()

    # return

def main():
    show_Up_UI()

def button_function(btn):
    btnClicked(btn)
    disable_buttons()

def disable_buttons():
    global root, button1, button2, button3, button4, button5, theLabel4
    button1.configure(state = 'disabled', background = "#808080")
    button2.configure(state = 'disabled', background = "#808080")
    button3.configure(state = 'disabled', background = "#808080")
    button4.configure(state = 'disabled', background = "#808080")
    button6.configure(state = 'disabled', background = "#808080")

    helv3 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)

    theLabel4 = Label(root, text="Now please show the card to the Robot and click Next", font = helv3)
    theLabel4.pack()
    theLabel4.place(x=530, y=500)


    button5 = Button(root, text="Next", height = 3, width = 30, command = changePage)
    button5.pack()
    button5.place(x = 900, y=650)


    # root.mainloop()

    # button5.configure(state = 'active')

def btnClicked(btn):
    # global count
    global names1
    print("you pressed the button " + btn)

    # display the answer chosen at the bottom
    theLabel3 = Label(root, text="You answer is: " + btn)
    theLabel3.pack()
    theLabel3.place(x= 650, y=600)

    names1.append(btn)

    np.savetxt("UI.txt", [btn], "%s")
    # names1.append(btn)
    # count +=1
    #
    # np.savetxt("C:\Users\nawam\PycharmProjects\NAO\User Interface data\Users_Chosen_Answers.txt", names1, delimiter= " ", newline= "\n" , fmt = "%s" )


if __name__ == "__main__":
    main()




