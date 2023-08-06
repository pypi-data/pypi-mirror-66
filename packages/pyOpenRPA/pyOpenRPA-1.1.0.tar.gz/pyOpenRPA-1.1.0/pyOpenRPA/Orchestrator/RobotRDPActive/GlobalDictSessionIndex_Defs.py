# ATTENTION! HERE IS NO Relative import because it will be imported dynamically
# All function check the flag SessionIsWindowResponsibleBool == True else no cammand is processed
# All functions can return None, Bool or Dict { "IsSuccessful": True }
from pyOpenRPA.Tools.RobotRDPActive import CMDStr # Create CMD Strings
from pyOpenRPA.Tools.RobotRDPActive import Connector # RDP API
def ProcessStartIfNotRunning(inGlobalDict, inSessionIndex, inProcessName, inFilePath, inFlagGetAbsPath=True):
    lResult = True
    lCMDStr = CMDStr.ProcessStartIfNotRunning(inProcessName,inFilePath, inFlagGetAbsPath= inFlagGetAbsPath)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RDPList"][inSessionIndex]["SessionHex"]
    # Check is Session is responsible
    if inGlobalDict["RDPList"][inSessionIndex]["SessionIsWindowResponsibleBool"]:
        # Run CMD
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN")
    else:
        # Write in logger - warning
        inGlobalDict["Logger"].warning(f"GlobalDictSessionIndex_Defs.ProcessStartIfNotRunning: SessionIndex: {str(inSessionIndex)}, ProcessName: {inProcessName}:: Session is not responsible!")
        lResult = False # Set false result - function has not been done
    return lResult
# Create CMD str to stop process
def ProcessStop(inGlobalDict, inSessionIndex, inProcessName, inFlagForceClose):
    lResult = True
    lCMDStr = f'taskkill /im "{inProcessName}" /fi "username eq %USERNAME%"'
    if inFlagForceClose:
        lCMDStr+= " /F"
        # Calculate the session Hex
    lSessionHex = inGlobalDict["RDPList"][inSessionIndex]["SessionHex"]
    # Check is Session is responsible
    if inGlobalDict["RDPList"][inSessionIndex]["SessionIsWindowResponsibleBool"]:
        # Run CMD
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN")
    else:
        # TODO Write in logger - warning
        inGlobalDict["Logger"].warning(f"GlobalDictSessionIndex_Defs.ProcessStop: SessionIndex: {str(inSessionIndex)}, ProcessName: {inProcessName}:: Session is not responsible!")
        lResult = False # Set false result - function has not been done
    return lResult
# Send file from Host to Session RDP using shared drive in RDP
def FileStoredSend(inGlobalDict, inSessionIndex, inHostFilePath, inRDPFilePath):
    lResult = True
    lCMDStr = CMDStr.FileStoredSend(inHostFilePath = inHostFilePath, inRDPFilePath = inRDPFilePath)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RDPList"][inSessionIndex]["SessionHex"]
    # Check is Session is responsible
    if inGlobalDict["RDPList"][inSessionIndex]["SessionIsWindowResponsibleBool"]:
        # Run CMD
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120)
    else:
        # Write in logger - warning
        inGlobalDict["Logger"].warning(f"GlobalDictSessionIndex_Defs.FileStoredSend: SessionIndex: {str(inSessionIndex)}, HostFilePath: {inHostFilePath}:: Session is not responsible!")
        lResult = False # Set false result - function has not been done
    return lResult
# Recieve file from Session RDP to Host using shared drive in RDP
def FileStoredRecieve(inGlobalDict, inSessionIndex, inRDPFilePath, inHostFilePath):
    lResult = True
    lCMDStr = CMDStr.FileStoredRecieve(inRDPFilePath = inRDPFilePath, inHostFilePath = inHostFilePath)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RDPList"][inSessionIndex]["SessionHex"]
    # Check is Session is responsible
    if inGlobalDict["RDPList"][inSessionIndex]["SessionIsWindowResponsibleBool"]:
        # Run CMD
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120)
    else:
        # Write in logger - warning
        inGlobalDict["Logger"].warning(f"GlobalDictSessionIndex_Defs.FileStoredRecieve: SessionIndex: {str(inSessionIndex)}, HostFilePath: {inHostFilePath}:: Session is not responsible!")
        lResult = False # Set false result - function has not been done
    return lResult