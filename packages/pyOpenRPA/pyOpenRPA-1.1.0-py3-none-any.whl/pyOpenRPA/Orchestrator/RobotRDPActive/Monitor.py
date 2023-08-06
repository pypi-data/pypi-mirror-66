from pyOpenRPA.Robot import UIDesktop
from . import Connector
import os
import time # Time wait operations
import importlib # from dynamic import module
from . import ConnectorExceptions # Exceptions classes


#Check for session is closed. Reopen if detected. Always keep session is active
def Monitor(inGlobalDict, inListUpdateTimeout):
    lFlagWhile = True
    lResponsibilityCheckLastSec = time.time() # Get current time for check interval
    while lFlagWhile:
        try:
            # UIOSelector list init
            lUIOSelectorList = []
            #Prepare selectors list for check
            for lIndex, lItem in enumerate(inGlobalDict["RDPList"]):
                lUIOSelectorList.append([{"title_re": f"{lItem['SessionHex']}.*", "backend": "win32"}])
            #Run wait command
            #import pdb
            #pdb.set_trace()
            lRDPDissappearList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List(lUIOSelectorList, inListUpdateTimeout)
            #print(lRDPDissappearList)
            ###########################################
            #Analyze if flag safeturn off is activated
            if inGlobalDict.get("OrchestratorToRobotResetStorage",{}).get("SafeTurnOff",False):
                lFlagWhile=False
                #Set status disconnected for all RDP List
                for lItem in inGlobalDict["RDPList"]:
                    lItem["SessionIsWindowExistBool"]=False
                    lItem["SessionIsWindowResponsibleBool"]=False
                #Kill all RDP sessions
                os.system('taskkill /F /im mstsc.exe')
                #Return from function
                return
            ###########################################
            ###########################################
            for lItem in lRDPDissappearList:
                inGlobalDict["RDPList"][lItem]["SessionIsWindowExistBool"] = False # Set flag that session is disconnected
                inGlobalDict["RDPList"][lItem]["SessionIsWindowResponsibleBool"]=False
                #pdb.set_trace()
                #Session start if it is not in ignore list
                #add check for selector if it is not in ignoreIndexList
                if lItem not in inGlobalDict["OrchestratorToRobotStorage"]["IgnoreIndexList"]:
                    try:
                        Connector.Session(inGlobalDict["RDPList"][lItem])
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowExistBool"] = True  # Flag that session is started
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowResponsibleBool"]= True
                        # Write in logger - info
                        inGlobalDict["Logger"].info(f"SessionHex: {str(inGlobalDict['RDPList'][lItem]['SessionHex'])}:: Session has been initialized!")
                    # catch ConnectorExceptions.SessionWindowNotExistError
                    except ConnectorExceptions.SessionWindowNotExistError as e:
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowExistBool"] = False # Set flag that session is disconnected
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowResponsibleBool"]=False
                        # Write in logger - warning
                        inGlobalDict["Logger"].warning(f"SessionHex: {str(inGlobalDict['RDPList'][lItem]['SessionHex'])}:: Session is not exist!")
                    # catch ConnectorExceptions.SessionWindowNotResponsibleError
                    except ConnectorExceptions.SessionWindowNotResponsibleError as e:
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowExistBool"] = True # Set flag that session is disconnected
                        inGlobalDict["RDPList"][lItem]["SessionIsWindowResponsibleBool"]=False
                        # Write in logger - warning
                        inGlobalDict["Logger"].warning(f"SessionHex: {str(inGlobalDict['RDPList'][lItem]['SessionHex'])}:: Session is not responsible!")
                    # general exceptions
                    except Exception as e:
                        # Write in logger - warning
                        inGlobalDict["Logger"].exception(f"!!! ATTENTION !!! Unrecognized error")
            #######################
            # Click all warning messages
            Connector.SystemRDPWarningClickOk()
            #######################
            ###########################################
            #Check if from Orchestrator full screen session is set
            if inGlobalDict["OrchestratorToRobotStorage"]["FullScreenSessionIndex"] != inGlobalDict["FullScreenSessionIndex"]:
                #Do some switches
                #If full screen mode we have now
                if inGlobalDict["FullScreenSessionIndex"] is not None:
                    if inGlobalDict["RDPList"][inGlobalDict["FullScreenSessionIndex"]]["SessionIsWindowExistBool"]:
                        Connector.SessionScreen100x550(inGlobalDict["RDPList"][inGlobalDict["FullScreenSessionIndex"]]["SessionHex"])
                #If new session is setted
                if inGlobalDict["OrchestratorToRobotStorage"]["FullScreenSessionIndex"] is not None:
                    if inGlobalDict["RDPList"][inGlobalDict["OrchestratorToRobotStorage"]["FullScreenSessionIndex"]]["SessionIsWindowExistBool"]:
                        Connector.SessionScreenFull(inGlobalDict["RDPList"][inGlobalDict["OrchestratorToRobotStorage"]["FullScreenSessionIndex"]]["SessionHex"])
                #Set one to other equal
                inGlobalDict["FullScreenSessionIndex"] = inGlobalDict["OrchestratorToRobotStorage"]["FullScreenSessionIndex"]
            ###########################################
            ####################################
            ##### Block check responsibility interval [ResponsibilityCheckIntervalSec]
            if inGlobalDict['ResponsibilityCheckIntervalSec']: # Do check if ResponsibilityCheckIntervalSec is not None
                if (time.time - lResponsibilityCheckLastSec()) > inGlobalDict['ResponsibilityCheckIntervalSec']:
                    # Set new time 
                    lResponsibilityCheckLastSec = time.time()
                    # Do responsibility check
                    for lIndex, lItem in enumerate(inGlobalDict["RDPList"]):
                        # Check RDP responsibility
                        lDoCheckResponsibilityBool = True
                        lDoCheckResponsibilityCountMax = 20
                        lDoCheckResponsibilityCountCurrent = 0
                        while lDoCheckResponsibilityBool:
                            # Enter full screen mode
                            Connector.SessionScreenFull(lItem['SessionHex'])
                            time.sleep(2)
                            # Check responding
                            lDoCheckResponsibilityBool = not Connector.SystemRDPIsResponsible()
                            # Check if counter is exceed - raise exception
                            if lDoCheckResponsibilityCountCurrent >= lDoCheckResponsibilityCountMax:
                                lItem["SessionIsWindowExistBool"] = False # Set flag that session is disconnected
                                lItem["SessionIsWindowResponsibleBool"]=False
                                # Session window is not responsible - restart RDP (close window here - next loop will reconnect)
                                Connector.SessionClose(lItem['SessionHex'])
                                # Turn off the loop 
                                lDoCheckResponsibilityBool = False
                            else:
                                # Exit fullscreen mode
                                Connector.SessionScreen100x550(lItem['SessionHex'])
                            # Wait if is not responding
                            if lDoCheckResponsibilityBool:
                                time.sleep(3)
                            # increase the couter
                            lDoCheckResponsibilityCountCurrent+=1
            ####################################
            # Check ActivityList from orchestrator
            lActivityListNew = []
            lActivityListOld = inGlobalDict["OrchestratorToRobotResetStorage"]["ActivityList"]+inGlobalDict["ActivityListStart"]
            inGlobalDict["ActivityListStart"] = []
            for lActivityItem in lActivityListOld:
                #################
                #Call function from Activity structure
                ################################################
                lSubmoduleFunctionName = lActivityItem["DefName"]
                lFileFullPath = lActivityItem["ModulePath"] # "path\\to\\module.py"
                lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                # Set gSettings in module
                lTechModuleFromSpec.gSettings = inGlobalDict
                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                    # Run SettingUpdate function in submodule
                    #mGlobalDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
                    lActivityItemResult=getattr(lTechModuleFromSpec, lSubmoduleFunctionName)(*lActivityItem["ArgList"],**lActivityItem["ArgDict"])
                    lActivityItemResultType = type(lActivityItemResult)
                    # Check if Result is bool
                    if lActivityItemResultType is bool:
                        if not lActivityItemResult:
                            # Activity is not done - add to list (retry in future)
                            lActivityListNew.append(lActivityItem)
                #################################################
            inGlobalDict["OrchestratorToRobotResetStorage"]["ActivityList"] = lActivityListNew # Override the value
        except RuntimeError as e:
            # case noGUI error passed - do nothing
            # Write in logger - warning
            inGlobalDict["Logger"].warning(f"Host session has lost the GUI")
        finally:
            # Wait for the next iteration
            time.sleep(0.7)
    return None
#TODO Def garbage window cleaner (if connection was lost)