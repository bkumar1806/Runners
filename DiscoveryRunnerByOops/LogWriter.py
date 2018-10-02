
import subprocess
import time
import os
import sys
import shutil
import re
import glob
import datetime
from Tkinter import *


class LogWriter:
    def __init__(self):
        self.sc_journal_path = sys.argv[2]
        self.ReportDate_n_Time = str(datetime.datetime.now())
        self.success_pattern = "Information: Journal.*Completed Successfully."
        self.fail_pattern = "Error: Journal Parse Error at step:.*"
        self.logFile = ""
        self.success = False
        self.successStringPartOne = """<SCENARIO ID="1" DESC="First Scenario......">        
        <ELAPSED>0.015</ELAPSED>
        <RESULT>PASSED</RESULT>
        </SCENARIO>
        <SCENARIO ID="2" DESC="Second Scenario.......">
        <PASS>"""
        self.successStringPartTwo = """</PASS>
        <ELAPSED>0.02</ELAPSED>
        <RESULT>PASSED</RESULT>
        <ARM_JOURNAL_COMPLETE />
        </SCENARIO>
        <ARM_ATTACHMENTS>
        <ATTACHMENT></ATTACHMENT>
        </ARM_ATTACHMENTS>
        <BUILD_DATES>
        <BUILD_DATE name="TimeTest">""" + self.ReportDate_n_Time + """</BUILD_DATE>
        </BUILD_DATES>"""

        self.failStringPartOne = """<SCENARIO ID="1" DESC="First Scenario.......">
        <ELAPSED>0.015</ELAPSED>
        <RESULT>PASSED</RESULT>
        </SCENARIO>
        <SCENARIO ID="2" DESC="Second Scenario.......">
        <Error>"""

        self.failStringPartTwo = """</Error>
        <ELAPSED>0.02</ELAPSED>
        <RESULT>ERROR</RESULT>
        <ARM_JOURNAL_COMPLETE />
        </SCENARIO>
        <ARM_ATTACHMENTS>
        <ATTACHMENT></ATTACHMENT>
        </ARM_ATTACHMENTS>
        <BUILD_DATES>
        <BUILD_DATE name="TimeTest">""" + self.ReportDate_n_Time + """</BUILD_DATE>
        </BUILD_DATES>"""

    def open_validation_log_file(self):
        self.logFile = open(ARM_WRK_DIR + "\\" + sys.argv[1] + "\\validation.log", 'w')

    def close_validation_log_file(self):
        self.logFile.close()

    def write_pass_fail_log(self):
        run_file_type = self.sc_journal_path.split(".")[1]
        if os.path.getsize(log_file_location) > 0:
            with open(log_file_location, "r") as app_data_log_file:
                log_file_lines = app_data_log_file.readlines()
                current_line = '\t'.join([line.strip() for line in log_file_lines])
                current_list = current_line.split("\t")
                for lin in current_list:
                    if run_file_type != "scjournal":
                        if "Script failed:" in lin:
                            script_pass = False
                            break
                    else:
                        if re.match(self.success_pattern, lin):
                            fhf = re.match(self.success_pattern, lin)
                            success_string = self.successStringPartOne + fhf.group() + self.successStringPartTwo
                            self.logFile.write(success_string)
                            self.success = True
                            break
                if script_pass and run_file_type != "scjournal":
                    success_string = self.successStringPartOne + " Script Passed " + self.successStringPartTwo
                    self.logFile.write(success_string)
                    self.success = True
                elif not script_pass and run_file_type != "scjournal":
                    fail_string = self.failStringPartOne + "Script Failed" + self.failStringPartTwo
                    self.logFile.write(fail_string)
                elif not self.success:
                    for lin in current_list:
                        if re.match(self.fail_pattern, lin):
                            fhf = re.match(fail_pattern, lin)
                            fail_string = self.failStringPartOne + fhf.group() + self.failStringPartTwo
                            self.logFile.write(fail_string)
                            log_writing = True
                            break
                    if not log_writing:
                        self.logFile.write(self.failStringPartOne + "Discovery Live session did not exit properly.Pease check LogFiles in AppData for details." + self.failStringPartTwo)
        self.close_validation_log_file()


class Utility:
    def __init__(self):
        self.UserInputPathSettingsFile = ""
        self.settingXmlPath = os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt"

    def getSettingXmlPath(self):
        def printtext():
            self.UserInputPathSettingsFile = E1.get()
            root.destroy()

        root = Tk()
        b = Button(root, text='Submit', command=printtext)
        b.pack(side='bottom')
        E1 = Entry(root, bd=5, font=14)
        E1.pack(side=BOTTOM)
        L1 = Label(root, text="Please enter the ARM Settings.xml path", font=14)
        L1.pack(side=BOTTOM)
        root.mainloop()

    def getWorkingDirectory(self):
        with open(open(os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt", "r").readline(), "r") as wrkdirfile:
            filelines = wrkdirfile.readlines()
            mystr = '\t'.join([line.strip() for line in filelines])
            mylist = mystr.split("\t")
            for lin in mylist:
                if re.match("<WORKING_DIR>.*</WORKING_DIR>", lin):
                    fhf = re.match("<WORKING_DIR>.*</WORKING_DIR>", lin)
                    return fhf.group()


class SCDMApplication:
    def __init__(self):
        self.SCJournalScenarios = []

    def getSCJounalScenario(self):
        with open(self.scjournalpath, "r") as scjournal:
            journal_steps = scjournal.readlines()
            for jou in journal_steps:
                if "UI_" in jou:
                    self.SCJournalScenarios.append(jou)

    def runDiscoveryWithJournal(self):
        proc = subprocess.check_call(
            '"' + scdminstall + '"' + " /RunApollo=true /UseSubscription=true" + " /J=" + scjournalpath + " /EXITAFTERJOURNAL=true",
            shell=True)


    def runDiscoveryWithScript(self):
        proc = subprocess.check_call(
            '"' + scdminstall + '"' + " /RunApollo=true /UseSubscription=true" + " /RunScript=" + scjournalpath + " /ExitAfterScript=true",
            shell=True)


if __name__ == "__main__":
    scdminstall = os.environ['AWP_ROOT192'] + "\\scdm\\SpaceClaim.exe"
    utility = Utility()
    scdm = SCDMApplication()
    logwriter = LogWriter()
    settingXmlPath = os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt"
    if not os.path.exists(settingXmlPath):
        utility.getSettingXmlPath()
    with open(os.getenv("APPDATA") + "\\ARM\\DiscoverySetting.txt", "w")as dsfile:
        dsfile.write(UserInputPathSettingsFile)
        dsfile.close()
    ARM_WRK_DIR = utility.getWorkingDirectory().split(">")[1].split("<")[0]
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
            scdm.runDiscoveryWithJournal()
        else:
            scdm.runDiscoveryWithScript()
    except:
        print("Error while running the journal file has occurred")
    finally:
        time.sleep(10)
        os.chdir(os.getenv("appdata") + "\\SpaceClaim\\Log Files")
        log_file_location = os.path.join(log_path, glob.glob("*.log")[0])
        # Script failed: unexpected EOF while parsing



























