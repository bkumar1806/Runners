from Tkinter import*
import os
string=""

def getSettingXmlPath():
    def printtext():
        global string
        string=E1.get()
        top.destroy()

    top = Tk()
    b = Button(top,text='Submit',command=printtext)
    b.pack(side='bottom')
    E1 = Entry(top, bd =5, font=14)
    E1.pack(side=BOTTOM)
    L1 = Label(top, text="Please enter the ARM Settings.xml path", font=14)
    L1.pack(side=BOTTOM)
    top.mainloop()

settingXmlPath = os.getenv("APPDATA")+"\\ARM\\DiscoverySetting.txt"
if not os.path.exists(settingXmlPath):
    getSettingXmlPath()
    string = 'r"'+string+'"'
    with open(os.getenv("APPDATA")+"\\ARM\\DiscoverySetting.txt","w")as dsfile:
        dsfile.write(string)
        dsfile.close()