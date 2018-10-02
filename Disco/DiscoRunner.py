# Scenarios fitting in String - third
# Trial running python exe without having python installed on the machine - first
# Part import in SCDM session - second
# Improvement in Dialogue box for setting xml - second - a-
# Running script via this arrangement - fourth
#

import subprocess
import time
import os
import sys
import shutil
import re
import glob
import datetime
from Tkinter import *

UserInputPathSettingsFile = ""
ReportDatenTime = str(datetime.datetime.now())
scjournalpath = sys.argv[2]
SCJournalScenarios = []
settingXmlPath = os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt"
disco_install = "E:\\Disco\\winx64\\Discovery.exe"

def getSettingXmlPath():
    def printtext():
        global UserInputPathSettingsFile
        UserInputPathSettingsFile = E1.get()
        root.destroy()

    root = Tk()
    b = Button(root, text='Submit', command=printtext)
    b.pack(side='bottom')
    E1 = Entry(root, bd=5, font=14)
    E1.pack(side=BOTTOM)
    L1 = Label(root, text="Please enter the ARM Settings.xml path", font=14)
    L1.pack(side=BOTTOM)
    root.mainloop()


def getWorkingDirectory():
    with open(open(os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt", "r").readline(), "r") as wrkdirfile:
        filelines = wrkdirfile.readlines()
        mystr = '\t'.join([line.strip() for line in filelines])
        mylist = mystr.split("\t")
        for lin in mylist:
            if re.match("<WORKING_DIR>.*</WORKING_DIR>", lin):
                fhf = re.match("<WORKING_DIR>.*</WORKING_DIR>", lin)
                return fhf.group()


def getSCJounalScenario():
    with open(scjournalpath, "r") as scjournal:
        journal_steps = scjournal.readlines()
        for jou in journal_steps:
            if "UI_" in jou:
                SCJournalScenarios.append(jou)


def runDiscoWithJournal():
    proc = subprocess.check_call(
        '"' + scdminstall + '"' + " /RunApollo=true /UseSubscription=true" + " /J=" + scjournalpath + " /EXITAFTERJOURNAL=true",
        shell=True)


def runDiscoWithScript():
    proc = subprocess.check_call(
        '"' + scdminstall + '"' + " /RunApollo=true /UseSubscription=true" + " /RunScript=" + scjournalpath + " /ExitAfterScript=true",
        shell=True)


if not os.path.exists(settingXmlPath):
    getSettingXmlPath()
    with open(os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt", "w")as dsfile:
        dsfile.write(UserInputPathSettingsFile)
        dsfile.close()

getSCJounalScenario()

ARM_WRK_DIR = getWorkingDirectory().split(">")[1].split("<")[0]
scriptPass = True
success_pattern = "Information: Journal.*Completed Successfully."
fail_pattern = "Error: Journal Parse Error at step:.*"
success = False
LogWriting = False
successStringPartOne = """<SCENARIO ID="1" DESC="First Scenario......">
<ELAPSED>0.015</ELAPSED>
<RESULT>PASSED</RESULT>
</SCENARIO>
<SCENARIO ID="2" DESC="Second Scenario.......">
<PASS>"""

successStringPartTwo = """</PASS>
<ELAPSED>0.02</ELAPSED>
<RESULT>PASSED</RESULT>
<ARM_JOURNAL_COMPLETE />
</SCENARIO>
<ARM_ATTACHMENTS>
<ATTACHMENT></ATTACHMENT>
</ARM_ATTACHMENTS>
<BUILD_DATES>
<BUILD_DATE name="TimeTest">""" + ReportDatenTime + """</BUILD_DATE>
</BUILD_DATES>"""

failStringPartOne = """<SCENARIO ID="1" DESC="First Scenario.......">
<ELAPSED>0.015</ELAPSED>
<RESULT>PASSED</RESULT>
</SCENARIO>
<SCENARIO ID="2" DESC="Second Scenario.......">
<Error>"""

failStringPartTwo = """</Error>
<ELAPSED>0.02</ELAPSED>
<RESULT>ERROR</RESULT>
<ARM_JOURNAL_COMPLETE />
</SCENARIO>
<ARM_ATTACHMENTS>
<ATTACHMENT></ATTACHMENT>
</ARM_ATTACHMENTS>
<BUILD_DATES>
<BUILD_DATE name="TimeTest">""" + ReportDatenTime + """</BUILD_DATE>
</BUILD_DATES>"""

journal_path = os.path.join(os.environ['appdata'], 'SpaceClaim', 'Journal Files')
print(journal_path)
try:
    if os.path.exists(journal_path):
        shutil.rmtree(journal_path)
except:
    print ("Journal files does not exist")

log_path = os.path.join(os.environ['appdata'], 'SpaceClaim', 'Log Files')

try:
    if os.path.exists(log_path):
        shutil.rmtree(log_path)
except:
    print ("Journal files does not exist")


try:
    if scjournalpath.split(".")[1] == "scjournal":
        runDiscoWithJournal()
    else:
        runDiscoWithScript()
except:
    print("Error while running the journal file has occurred")
finally:
    time.sleep(10)
    os.chdir(os.getenv("appdata") + "\\SpaceClaim\\Log Files")
    log_file_location = os.path.join(log_path, glob.glob("*.log")[0])
    # Script failed: unexpected EOF while parsing
    if os.path.getsize(log_file_location) > 0:
        print(os.path.getsize(log_file_location))
        with open(log_file_location, "r") as myfile:
            errormessage = myfile.readlines()
            mystr = '\t'.join([line.strip() for line in errormessage])
            mylist = mystr.split("\t")
            f = open(ARM_WRK_DIR + "\\" + sys.argv[1] + "\\validation.log", 'w')
            for lin in mylist:
                if scjournalpath.split(".")[1] != "scjournal":
                    if "Script failed:" in lin:
                        scriptPass = False
                        break
                else:
                    if re.match(success_pattern, lin):
                        fhf = re.match(success_pattern, lin)
                        successString = successStringPartOne + fhf.group() + successStringPartTwo
                        f.write(successString)
                        success = True
                        break
            if scriptPass and scjournalpath.split(".")[1] != "scjournal":
                successString = successStringPartOne + " Script Passed " + successStringPartTwo
                f.write(successString)
                success = True
            elif not scriptPass and scjournalpath.split(".")[1] != "scjournal":
                FailString = failStringPartOne + "Script Failed" + failStringPartTwo
                f.write(FailString)
            elif not success:
                for lin in mylist:
                    if re.match(fail_pattern, lin):
                        fhf = re.match(fail_pattern, lin)
                        FailString = failStringPartOne + fhf.group() + failStringPartTwo
                        f.write(FailString)
                        LogWriting = True
                        break
                if not LogWriting:
                    f.write(
                        failStringPartOne + "Discovery Live session did not exit properly.Pease check LogFiles in AppData for details." + failStringPartTwo)
        f.close()


























