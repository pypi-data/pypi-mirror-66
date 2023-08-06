#Import parent folder to import current / other packages
from pyOpenRPA.Robot import UIDesktop #Lib to access RDP window
from . import ConnectorExceptions # Exceptions classes
import os #os for process run
import uuid #temp id for Template.rdp
import tempfile #Temporary location
import subprocess
from . import Clipboard # Clipboard functions get/set
import keyboard # Keyboard functions
import time
import random # random integers
from win32api import GetSystemMetrics # Get Screen rect
#Connect to RDP session
"""
{
    "Host": "", #Host address
    "Port": "", #RDP Port
    "Login": "", # Login
    "Password": "", #Password
    "Screen": {
        "Resolution":"FullScreen", #"640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
        "FlagUseAllMonitors": False, # True or False
        "DepthBit":"" #"32" or "24" or "16" or "15"
    }
}
"""
def Session(inRDPSessionConfiguration):
    #RDPConnector.SessionConnect(mConfiguration)
    #RDPConnector.LoginPassSet("111.222.222.111","ww","dd")
    (lRDPFile, lSessionHex) = SessionConfigurationCreate(inRDPSessionConfiguration)
    #Set session hex in globalDict
    inRDPSessionConfiguration["SessionHex"] = lSessionHex
    #Set login/password
    SessionLoginPasswordSet(inRDPSessionConfiguration["Host"],inRDPSessionConfiguration["Login"],inRDPSessionConfiguration["Password"])
    #Start session
    SessionRDPStart(lRDPFile)
    #Remove temp file
    time.sleep(4) #Delete file after some delay - one way to delete and run the RDP before because RDP is not read file in one moment
    os.remove(lRDPFile) # delete the temp rdp
    # Set the result 
    return inRDPSessionConfiguration
#Add login/ password to the windows credentials to run RDP
def SessionLoginPasswordSet(inHost, inLogin, inPassword):
    #Clear old login/password if it exists
    #os.system(f"cmdkey /delete:TERMSRV/{inHost}") #Dont need to delete because new user password will clear the previous creds
    #Set login password for host
    os.system(f'cmdkey /generic:TERMSRV/{inHost} /user:{inLogin} /pass:"{inPassword}"')
    return None
#Create current .rdp file with settings
#Return (full path to file, session hex)
def SessionConfigurationCreate(inConfiguration):
    #RobotRDPActive folder path
    lFileFullPath=__file__
    lFileFullPath = lFileFullPath.replace("/","\\")
    lRobotRDPActiveFolderPath = "\\".join(lFileFullPath.split("\\")[:-1])
    #Full path to Template.rdp file
    lRDPTemplateFileFullPath = os.path.join(lRobotRDPActiveFolderPath, "Template.rdp")
    #Open template file (.rdp encoding is USC-2 LE BOM = UTF-16 LE) http://qaru.site/questions/7156020/python-writing-a-ucs-2-little-endian-utf-16-le-file-with-bom
    lRDPTemplateFileContent = open(lRDPTemplateFileFullPath, "r", encoding="utf-16-le").read()
    #Prepare host:port
    lHostPort=inConfiguration['Host']
    if 'Port' in inConfiguration:
        if inConfiguration['Port']:
            lHostPort=f"{lHostPort}:{inConfiguration['Port']}"
    # Generate parameter for .rdp "drivestoredirect:s:C:\;"
    lDriveStoreDirectStr = ""
    for lItem in inConfiguration['SharedDriveList']:
        lDriveStoreDirectStr+=f"{lItem.upper()}:\\;" # Attention - all drives must be only in upper case!!!
    #Replace {Width}, {Height}, {BitDepth}, {HostPort}, {Login}
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Width}", str(inConfiguration.get('Screen',{}).get("Width",1680)))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Height}", str(inConfiguration.get('Screen',{}).get("Height",1050)))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{BitDepth}", inConfiguration.get('Screen',{}).get("DepthBit","32"))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{HostPort}", lHostPort)
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Login}", inConfiguration['Login'])
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{SharedDriveList}", lDriveStoreDirectStr)
    #Save template to temp file
    lRDPCurrentFileFullPath = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.rdp")
    open(lRDPCurrentFileFullPath, "w", encoding="utf-16-le").write(lRDPTemplateFileContent)
    #Return .rdp full path
    return (lRDPCurrentFileFullPath, (lRDPCurrentFileFullPath.split("\\")[-1])[0:-4])
#RDPSessionStart
def SessionRDPStart(inRDPFilePath):
    #Disable certificate warning
    lCMDString = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client" /v "AuthenticationLevelOverride" /t "REG_DWORD" /d 0 /f'
    os.system(lCMDString)
    #run rdp session
    lItemArgs = [inRDPFilePath]
    subprocess.Popen(lItemArgs, shell=True)
    #Wait for UAC unknown publisher exists
    lRDPFileName = (inRDPFilePath.split("\\")[-1])[0:-4]
    lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
        [
            [{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
             {"title": "Боль&ше не выводить запрос о подключениях к этому компьютеру", "friendly_class_name": "CheckBox"}],
            [{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
             {"title": "D&on't ask me again for connections to this computer",
              "friendly_class_name": "CheckBox"}],
            [{"title_re": f"{lRDPFileName}.*",
              "class_name": "TscShellContainerClass", "backend": "win32"},{"depth_start":3, "depth_end": 3, "class_name":"UIMainClass"}]
        ],
        30
    )    
    #Enable certificate warning
    lCMDString = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client" /v "AuthenticationLevelOverride" /t "REG_DWORD" /d 2 /f'
    os.system(lCMDString)
    #Click if 0 is appear (RUS)
    if 0 in lWaitResult:
        #Check the box do not retry
        UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "backend": "win32"},
             {"title": "Боль&ше не выводить запрос о подключениях к этому компьютеру", "friendly_class_name": "CheckBox"}]).check()
        #Go to connection
        UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "backend": "win32"},
             {"title":"Подкл&ючить", "class_name":"Button"}]).click()
        lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
            [
                [{"title_re": f"{lRDPFileName}.*",
                  "class_name": "TscShellContainerClass", "backend": "win32"}]
            ],
            30
        )
    # Click if 1 is appear (ENG)
    if 1 in lWaitResult:
        # Check the box do not retry
        UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
             {"title": "D&on't ask me again for connections to this computer",
              "friendly_class_name": "CheckBox"}]).check()
        # Go to connection
        UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                                       {"title": "Co&nnect", "class_name": "Button"}]).click()
        lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
            [
                [{"title_re": f"{lRDPFileName}.*",
                  "class_name": "TscShellContainerClass", "backend": "win32"}]
            ],
            30
        )
    # Raise exception if RDP is not active
    if len(lWaitResult) == 0:
        raise ConnectorExceptions.SessionWindowNotExistError("Error when initialize the RDP session - No RDP windows has appreared!")
    # Wait for init
    time.sleep(3)
    SessionScreenSize_X_Y_W_H(inSessionHex = lRDPFileName, inXInt = 10, inYInt = 10, inWInt = 550, inHInt = 350) #Prepare little window
    return None

#Set fullscreen for app
def SessionScreenFull(inSessionHex):
    #Prepare little window
    try:
        lRDPWindow = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHex}.*", "backend": "win32"}])
    except Exception as e:
        return None
    lRDPWindow.set_focus()
    lRDPWindow.maximize()
    #time.sleep(0.5)
    if not SessionIsFullScreen(inSessionHex):
        lRDPWindow.type_keys("^%{BREAK}")
        time.sleep(0.5)
    return None

# Set the screen size
def SessionScreenSize_X_Y_W_H(inSessionHex, inXInt, inYInt, inWInt, inHInt):
    lDoBool = True
    while lDoBool:
        #Prepare little window
        try:
            lRDPWindow = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHex}.*", "backend": "win32"}])
        except Exception as e:
            return None
        try:
            lRDPWindow.set_focus()
            if SessionIsFullScreen(inSessionHex):
                lRDPWindow.type_keys("^%{BREAK}")
            time.sleep(0.5)
            lRDPWindow.restore()
            time.sleep(0.5)
            lRDPWindow.move_window(inXInt,inYInt,inWInt,inHInt)
        except Exception as e:
            time.sleep(1)
        else:
            lDoBool = False
    return None

# Set Little window of the session
def SessionScreen100x550(inSessionHex):
    SessionScreenSize_X_Y_W_H(inSessionHex = inSessionHex, inXInt = 10, inYInt = 10, inWInt = 550, inHInt = 100)
    return None
# Session - close window
def SessionClose(inSessionHexStr):
    #Close window
    try:
        UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}]).close()
    except Exception as e:
        pass
#Type command in CMD
# inSessionHex - SessionHex to catch window
# inModeStr "LISTEN", "CROSSCHECK", "RUN"
#   "LISTEN" - Get result of the cmd command in result TODO get home script
#   "CROSSCHECK" - Check if the command was successufully sent TODO get home script
#   "RUN" - Run without crosscheck and get clipboard
# return {
#   "OutStr": <> # Result string
#   "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
# }
# example Connector.SessionCMDRun("4d1e48f3ff6c45cc810ea25d8adbeb50","start notepad", "RUN")
def SessionCMDRun(inSessionHex,inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK", inClipboardTimeoutSec = 5):
    # Init the result dict
    lResult = {"OutStr": None,"IsResponsibleBool":True}
    # Enter full screen mode
    SessionScreenFull(inSessionHex)
    time.sleep(2)
    # Run CMD operations
    lResult = SystemCMDRun(inCMDCommandStr = inCMDCommandStr, inModeStr = inModeStr, inClipboardTimeoutSec = inClipboardTimeoutSec)
    # Exit fullscreen mode
    SessionScreenSize_X_Y_W_H(inSessionHex=inSessionHex, inXInt=10, inYInt=10, inWInt=550,
                              inHInt=350)  # Prepare little window
# Check if session is in Full screen mode
# Return True - is in fullscreen
# example print(Connector.SessionIsFullScreen(""))
def SessionIsFullScreen(inSessionHexStr):
    #Default resul
    lResult = False
    lWeight = GetSystemMetrics(0)
    lHeight = GetSystemMetrics(1)
    #Get window screen
    try:
        lRectangle = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}]).rectangle()
    except Exception as e:
        return lResult
    # Get Height/Weight
    lSessionWeight = lRectangle.right - lRectangle.left
    lSessionHeight = lRectangle.bottom - lRectangle.top
    #Case fullscreen
    if lSessionHeight == lHeight and lSessionWeight == lWeight:
        lResult = True
    return lResult
# Check if RDP session is responsible (check with random combination in cmd)
# Attention - function will be work fine if RDP will be in full screen mode!!! (see def SessionScreenFull)
# Return True - is responsible; False - is not responsible
#Type command in CMD
# inFlagDoCrossCheck: True - Do check that CMD is executed (the text response will not be available)
# inModeStr "LISTEN", "CROSSCHECK", "RUN"
#   "LISTEN" - Get result of the cmd command in result TODO get home script
#   "CROSSCHECK" - Check if the command was successufully sent TODO get home script
#   "RUN" - Run without crosscheck and get clipboard
# inClipboardTimeoutSec # Second for wait when clipboard will changed
# return {
#   "OutStr": <> # Result string
#   "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
# }
# example Connector.SessionCMDRun("4d1e48f3ff6c45cc810ea25d8adbeb50","start notepad", "RUN")
def SystemCMDRun(inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK", inClipboardTimeoutSec = 5):
    # Set random text to clipboard (for check purposes that clipboard text has been changed)
    lClipboardTextOld = str(random.randrange(999,9999999))
    Clipboard.TextSet(lClipboardTextOld)
    # Init the result dict
    lResult = {"OutStr": None,"IsResponsibleBool":True}
    lCrosscheckKeyStr = str(random.randrange(999,9999999))
    lCMDPostFixStr = "" # Case default "RUN"
    if inModeStr == "CROSSCHECK":
        lCMDPostFixStr = f"| echo {lCrosscheckKeyStr} | clip"
    elif inModeStr == "LISTEN":
        lCMDPostFixStr = f"| clip"
    keyboard.press_and_release('win+r')
    time.sleep(1)
    # Remove old text
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("backspace")
    # Write new text
    keyboard.write(f"cmd /c {inCMDCommandStr} {lCMDPostFixStr}")
    time.sleep(1)
    # TODo cross check from clipboard
    keyboard.press_and_release('enter')
    # Get OutStr (Case CROSSCHECK and LISTEN)
    if inModeStr == "CROSSCHECK" or inModeStr == "LISTEN":
        lClipboardWaitTimeStartSec = time.time()
        lResult["OutStr"] = Clipboard.TextGet() # Get text from clipboard
        while lResult["OutStr"] == lClipboardTextOld and (time.time() - lClipboardWaitTimeStartSec) <= inClipboardTimeoutSec:
            lResult["OutStr"] = Clipboard.TextGet() # Get text from clipboard
            time.sleep(0.5) # wait some time for the next operation
    # Do crosscheck 
    if inModeStr == "CROSSCHECK":
        if lResult["OutStr"] == f"{lCrosscheckKeyStr} \r\n\x00\x00\x00\x00\x00":
            lResult["IsResponsibleBool"] = True
        else:
            lResult["IsResponsibleBool"] = False
    # return the result
    return lResult
# Check if current RDP is responsible
def SystemRDPIsResponsible():
    return SystemCMDRun(inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK")["IsResponsibleBool"]
# Click OK on error messages
def SystemRDPWarningClickOk():
    # Try to click OK Error window in RUS version
    while UIDesktop.UIOSelector_Exist_Bool([{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
             {"title": "ОК", "class_name": "Button"}]):
        try:
            UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
                 {"title": "ОК", "class_name": "Button"}]).click()
        except Exception as e:
            pass
    # Try to click OK Error window in ENG version
    while UIDesktop.UIOSelector_Exist_Bool([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                 {"title": "OK", "class_name": "Button"}]):
        try:
            UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                 {"title": "OK", "class_name": "Button"}]).click()
        except Exception as e:
            pass