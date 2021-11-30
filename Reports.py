from ReportStage import ReportStage, ReportPrompt
from User import User
from typing import Final
import os
import pathlib
import jsonpickle

from Utils import console, LogType

class Reports:
    
    Path : Final = pathlib.Path(__file__).parent.resolve()/"Reports" #path locale dove salvare i json dei report
    DataPath : Final = pathlib.Path(__file__).parent.resolve()/"Reports"/"users.data"
    
    users = dict()
    
    def __init__(self):
        #Legge i dati da disco se disponibili
        if not os.path.exists(str(self.Path)):
            os.makedirs(str(self.Path))
        if os.path.exists(str(self.DataPath)):
            self.Load()
    
    def Save(self):
        f = open(str(self.DataPath), "w")
        f.write(jsonpickle.encode(self.users))
        f.close()
    
    def Load(self):
        f = open(str(self.DataPath), "r")
        self.users = jsonpickle.decode(f.read())
        f.close()
    
    def IsUserEnabled(self, Id : int):
        if not self.GetUser(Id) == None: 
                return True
        return False
    
    def AddUser(self, Id : int, Name : str, DisplayName : str, PreferredWeekday : int or None = None):
        self.users[Id] = User(Id,Name, DisplayName, PreferredWeekday)
        self.Save()
    
    def GetUser (self, Id : int):
        try:
            return self.users[Id]
        except:
            return None
    
    def GetUsers (self):
        return self.users
    
    def GetUserStagePrompt (self, Id : int):
        return self.GetUser(Id).reportPrompt
    
    def GetUserStage(self, Id : int):
        return self.GetUser(Id).reportStage
    
    def GetUserAnswers(self, Id : int):
        return self.GetUser(Id).GetAnswers()
    
    def SetUserDisplayName(self, Id : int, DisplayName : str): 
        if self.GetUser(Id) == None:
            return
        self.GetUser(Id).displayName = DisplayName
        
    def ResetUserStage(self, Id : int):
        self.GetUser(Id).ResetStage()
        
    def HasUserDone (self, Id : int):
        if self.GetUserStage(Id) == ReportStage.DONE:
            return True
        return False
    
    def AdvanceUserStage(self, Id : int):
        self.GetUser(Id).AdvanceStage()
    
    def RegisterUserAnswer(self, Id : int, Answer : str):
        self.GetUser(Id).RegisterAnswer(Answer)
        self.Save()