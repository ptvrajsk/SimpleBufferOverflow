import subprocess
import sys
import re
import os
import xml.etree.ElementTree as ET

##################################################
################ FUZZER CONSTANTS ################
##################################################
class CONST_MGR:

    def __init__(self):
        self.SCRIPT_ARGS = 3
        self.BUTTON_CLASS = "android.widget.Button"
        self.EDITTEXT_CLASS = "android.widget.EditText"
        self.TMP_WD = f"{os.path.dirname(os.path.abspath(__file__))}/tmp"
        self.TMP_FD = f"{self.TMP_WD}/tmp.xml"
        self.LOG_FD = f"{self.TMP_WD}/crashlog.txt"
        self.MAL_INPUT_FD = f"{self.TMP_WD}/maliciousInput.txt"

CONST = CONST_MGR()


#################################################
########### STDOUT FORMATTING OPTIONS ###########
#################################################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

##############################################
############## HELPER FUNCTIONS ##############
##############################################

def getAverageCoordinateFromBounds(bounds):
    boundMatches = re.search("\\[([0-9]*),([0-9]*)\\]\\[([0-9]*),([0-9]*)\\]", bounds)
    averageX = str((int(boundMatches.group(1)) + int(boundMatches.group(3))) / 2)
    averageY = str((int(boundMatches.group(2)) + int(boundMatches.group(4))) / 2)
    return (averageX, averageY)

def getSubmitButtonCoordinates():
    root = ET.parse(CONST.TMP_FD).getroot()
    # foundButton = False
    for node in root.iter("node"):
        nodeAttrs = node.attrib
        if nodeAttrs["class"] == CONST.BUTTON_CLASS:
            return getAverageCoordinateFromBounds(node.attrib["bounds"])
    ### Use for debugging (if the script is not responding properly)
    # if not foundButton:
    #     print(
    #         bcolors.FAIL +
    #         "Unable to find button to submit input!" +
    #         bcolors.ENDC +
    #         bcolors.WARNING +
    #         "Application has crashed perhaps?" +
    #         bcolors.ENDC
    #     )

def findUiHierarchyLocationOnDevice():
    getButtonDataCmd="adb shell uiautomator dump"
    rawButtonData = subprocess.check_output(getButtonDataCmd.split()).decode("utf-8")
    return re.findall("(\\/.*)", rawButtonData)[0]

def inputTextAndHideKeyboard(text):
    sendTextInput = f"adb shell input text {text}"
    subprocess.check_output(sendTextInput.split())
    hideKeyboard = "adb shell input keyevent 111"
    subprocess.check_output(hideKeyboard.split())

#################################################
################# FUZZER SCRIPT #################
#################################################

if sys.argv[1] == "--help":
        print(
            bcolors.BOLD +
            bcolors.OKBLUE +
            f"\nUsage: python3 {os.path.basename(__file__)} <package_name> <min_input_len>" +
            bcolors.ENDC
        )
        print (
            f"<package_name>" +
            f": Refers to the app package name that fuzzer should work on."
        )
        print (
            f"<min_input_len>" +
            f": Refers to the minimum length of input to be used in brute-forcing text.\n"
        )
        sys.exit()
elif len(sys.argv) != CONST.SCRIPT_ARGS:
    print(
        bcolors.FAIL +
        f"\nThere should be {CONST.SCRIPT_ARGS - 1} argument(s) supplied to the script" +
        bcolors.ENDC
    )
    print(
        bcolors.WARNING +
        "Use --help for more information\n" +
        bcolors.ENDC
    )
    sys.exit()

# Initialize tmp directory for files
try:
    print(f"New working directory created at: {CONST.TMP_WD}\n")
    os.mkdir(CONST.TMP_WD)
except FileExistsError:
    pass
except:
    print(
        bcolors.FAIL +
        f"Unable to create temp. working directory at: {CONST.TMP_WD}\n" +
        bcolors.ENDC
    )
    sys.exit()

# Launch App (Can't seem to supress this info but not going to look into it cause its not too important now)
print("Launching App..")
appLaunchCommand = f"adb shell monkey -p {sys.argv[1]} -c android.intent.category.LAUNCHER 1"
subprocess.run(appLaunchCommand.split(), stdout=subprocess.DEVNULL)
print("\n")

# Prep for Fuzzing
counter = int(sys.argv[2])
inputString = "a" * (counter - 1)
inputTextAndHideKeyboard(inputString)

getAppProcInfo = f"adb shell pidof {sys.argv[1]}"
rawProcessInfo = subprocess.check_output(getAppProcInfo.split())

try:
    while rawProcessInfo != "":
        
        ### Check coordinates of button each iteration to
        ### correct for shifts in the ui.
        
        # Get Ui Hierarchy Information Location
        uiHierarchyLoc = findUiHierarchyLocationOnDevice()

        # Download Heirarchy Information
        getUiHeirarchyInfo = f"adb pull {uiHierarchyLoc} {CONST.TMP_FD}"
        rawButtonData = subprocess.check_output(getUiHeirarchyInfo.split())
        (btnX, btnY) = getSubmitButtonCoordinates()
        
        ### Begin Fuzzing

        # Track Input Size
        counter = counter + 1
        
        # Input Next Attack String
        inputTextAndHideKeyboard("a")

        # Submit Input
        tapSubmitButton = f"adb shell input tap {btnX} {btnY}"
        subprocess.check_output(tapSubmitButton.split())
        
        # Check if Process Crashed
        rawProcessInfo = subprocess.check_output(getAppProcInfo.split())
except subprocess.CalledProcessError:
    pass
except TypeError:
    pass

## CRASH LOG
outputCrashLog = f"adb logcat -d"
crashLog = subprocess.check_output(outputCrashLog.split()).decode("utf-8")

crashLogFile = open(CONST.LOG_FD, "w+")
crashLogFile.write(crashLog)
crashLogFile.close()
print(f"CrashLog Deposit: {CONST.LOG_FD}\n")

## Malicious Input
inputString = "a" * counter
maliciousInputFileContent = [f"Length of Malicious Input: {counter}\n", f"Malicious Input: {inputString}\n"]

maliciousInputFile = open(CONST.MAL_INPUT_FD, "w+")
maliciousInputFile.writelines(maliciousInputFileContent)
maliciousInputFile.close()
print(f"Malicious Input Deposit: {CONST.MAL_INPUT_FD}\n")

