#********************************************************************
#	created:	13/08/2021
#	file base:	Main
#	file ext:	py
#	author:		Alessandro Brancaccio
#	version:	1.0.3
#	
#	purpose:	Misc utils
#*********************************************************************

from enum import Enum
import logging
import os
from datetime import datetime
from typing import Final

#--------------------------------Variabili

#altre impostazioni
workingDirectory : Final = "C:/try-it-on"
is_Debug : Final = True #Utile per abilitare o disabilitare comportamenti di test
logPath : Final = "log.txt"
logLevel : Final = logging.DEBUG #logga tutto
#logPath : Final = "sdcard/YoubiquoSRL/Try-It-On/log.txt" #android log path
#logLevel : Final = logging.WARN #logga dai warn in poi

#--------------------------------Classi

"""[summary]
    Il livello di severità del log
Returns:
    [type]: [description]
"""
class LogType(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

#--------------------------------Funzioni
    """[summary]Scrive su console.
    """
def console (Severity = LogType.ERROR, Tag = "", Content = ""):
    if Severity == LogType.DEBUG and is_Debug:
        print(f'[DEBUG][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    elif Severity == LogType.INFO:
        print(f'[INFO][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    elif Severity == LogType.WARN:
        print(f'[WARNING][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    else:
        print(f'[ERROR][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')

"""[summary]Scrive su console e file di log.
    """
def log(Severity = LogType.ERROR, Tag = "", Content = ""):
    if Severity == LogType.DEBUG and is_Debug:
        logging.debug(f'[DEBUG][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    elif Severity == LogType.INFO:
        logging.info(f'[INFO][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    elif Severity == LogType.WARN:
        logging.warning(f'[WARNING][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    else:
        logging.error(f'[ERROR][{datetime.now().strftime("%H:%M:%S")}][{Tag}] {Content}')
    console(Severity, Tag, Content)

"""[summary] Inizializza il log.
    """
def log_init ():
    global logPath
    global logLevel
    InitializePath(workingDirectory)
    logging.basicConfig(filename=workingDirectory+"/"+logPath, filemode='w', level=logLevel)

"""[summary]Inizializza un percorso.
    """
def InitializePath(DirectoryPath:str, FileName:str = None):
    if not os.path.isdir(DirectoryPath):
        os.mkdir(DirectoryPath)
    if FileName != None:
        if not os.path.isfile(DirectoryPath+"/"+FileName):
            tmp = open(DirectoryPath+"/"+FileName, "x")
            tmp.close()

"""[summary]Verifica se esiste un file flag.
    """
def VerifyFileFlag(FilePath:str):
    if os.path.exists(FilePath):
        os.remove(FilePath)
        return True
    return False