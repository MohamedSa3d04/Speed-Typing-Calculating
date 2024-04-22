#import libraries
from tkinter import *
from tkinter import ttk
import datetime 
import random

root = Tk()

# Getting random text:
sentents = open(r'projects\sentents.txt', mode='r').read().split("\n") #You can edit (sentents.txt) for any text
class Board :
    def __init__(self, root):
        #Intializing the screen
        self.root = root
        self.root.geometry('800x650+350+50') 
        self.root.resizable(False,False) 
        self.root.title("Type Speed Calc V1.0") 
        self.root.config(background='gray') 
        #Intializing the important variables
        self.sentense = random.choice(sentents)
        self.CurPosition = 0
        self.counterChars = 0
        self.counterWords = 2
        self.TestNumber = 0
        self.Records = [] #Number of CPMs
        self.CPS = 0
        self.CPM = self.CPS * 60
        self.WPS = 0
        self.WPM = self.WPS * 60

        #Sentense Frame
        self.senFrame = Frame(self.root)
        self.senFrame.pack(expand=True)

        self.lblsen = Label(self.root, text=f'{self.sentense}', font=('Cascadia Code', 20,'bold'), width=40,height=5, justify='center', wraplength=470)
        self.lblsen.place(x=80,y=30)
        
        #Sentense Input Entry
        self.senInput = Entry(self.senFrame, font=('Cascadia Code', 20), width=40)
        self.senInput.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.senInput.bind("<KeyRelease>", self.checkChar)
        
        #label for calculations
        self.lblCalcs = Label(self.senFrame,font=('Cascadia Code',15), text=f"CPS : {self.CPS}\nCPM : {self.CPM}\nWPS : {self.WPS}\nWPM : {self.WPM}")
        self.lblCalcs.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        #reseting the screen (with new sen)
        self.btnReset = Button(self.root, text='Reset', bg='#E9CF88', font=('Arial', 15), border=0,width=20, command=self.Reset)
        self.btnReset.place(x=290,y=450)

        #Results Frame
        self.resFrame = Frame(self.root, bg='#E9CF88',width=800 ,height=45)
        self.resFrame.pack()
        
        self.lblres1 = Label(self.resFrame,bg='#E9CF88', font=('consolas',15), text=f'Best Record: CPS : {self.CPS} CPM : {self.CPM} WPS : {self.WPS} WPM : {self.WPM}')
        self.lblres1.place(x=2,y=10)


    #Defining the Algorithm
    def checkChar(self, char):
        self.CurSentence = self.senInput.get() #Current sentense input
        self.CurPosition = len(self.CurSentence) - 1 #Current position typing
        self.backnum = 0 #Number of time clicking BackSpace
        if self.counterChars == 0:#For calculating start time writing
            self.startTime = datetime.datetime.now()
        if (char.keycode >= 65 and char.keycode <= 90) or char.char in [",",'-',":",'.'] or char.keycode == 32:
            self.CurPosition += 1 
            if self.CurSentence == self.sentense[:self.CurPosition]: #When True Typing
                if char.char == " ":
                    self.counterWords += 1
                self.counterChars += 1
                self.senInput.config(fg='green')
            else:
                self.senInput.config(fg='red')
            endTime = datetime.datetime.now()# Refrishing now time in each  char
            self.diffTime = endTime - self.startTime
            self.CPS = self.counterChars / (self.diffTime.total_seconds() + 0.0001)
            self.WPS = self.counterWords / (self.diffTime.total_seconds() + 0.0001)
            self.lblCalcsConfig()  #Refrishing calculations label
            
            if self.CurSentence == self.sentense:  #User end the task 
                self.senInput.unbind('<KeyRelease>')
                self.senInput.config(state='readonly')
                if self.TestNumber == 0:
                    self.lblres1.config(text=f'Best Record: CPS : {self.CPS.__round__(3)} CPM : {self.CPM.__round__(3)} WPS : {self.WPS.__round__(3)} WPM : {self.WPM.__round__(3)}')
                    self.firstRec = self.CPS
                    self.Records.append(self.firstRec)
                else:
                    lastCPS = self.CPS
                    if lastCPS > self.Records[-1]:
                        self.Records.append(lastCPS)
                        #Refreshing the result label for each round only if new record broked
                        self.lblres1.config(text=f'Best Record: CPS : {self.CPS.__round__(3)} CPM : {self.CPM.__round__(3)} WPS : {self.WPS.__round__(3)} WPM : {self.WPM.__round__(3)}')
                self.TestNumber += 1

        elif char.keycode == 8: #When clicking back-space
            if self.CurSentence == self.sentense[:self.CurPosition+1]:
                self.senInput.config(fg='green') 
            else:
                self.senInput.config(fg='red')
        else:
            self.senInput.config(fg='red')
        
    def lblCalcsConfig(self): #Refrishing calculations label
        self.CPM = self.CPS * 60
        self.WPM = self.WPS * 60
        self.lblCalcs.config(text=f"CPS : {self.CPS.__round__(3)}\nCPM : {self.CPM.__round__(3)} \nWPS : {self.WPS.__round__(3)}\nWPM : {self.WPM.__round__(3)}")
   
    def Reset(self): 
        self.sentense = random.choice(sentents)
        self.CurPosition = 0
        self.counterChars = 0
        self.counterWords = 0
        self.CPS = 0
        self.CPM = 0
        self.WPS = 0
        self.WPM = 0

        self.lblsen.config(text=f'{self.sentense}')
        self.senInput.config(state='normal', fg='black')
        self.senInput.delete(0, 'end')

        self.lblCalcs.config(text=f"CPS : {self.CPS}\nCPM : {self.CPM}\nWPS : {self.WPS}\nWPM : {self.WPM}")
        self.senInput.bind("<KeyRelease>", self.checkChar)

board = Board(root)
root.mainloop()