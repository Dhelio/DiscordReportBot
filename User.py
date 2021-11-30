

from ReportStage import ReportPrompt, ReportStage


class User:
    
    id : int
    name : str
    displayName : str
    reportStage : ReportStage
    reportPrompt : ReportPrompt
    preferredWeekday : int
    answers = []
    
    def __init__(self, id : int, name : str, displayName : str, preferredWeekday : str = None):
        self.id = id
        self.name = name
        self.displayName = displayName
        if preferredWeekday is None:
            self.preferredWeekday = 4
        else:
            self.preferredWeekday = preferredWeekday
        self.reportStage = ReportStage.DONE
        self.reportPrompt = ReportPrompt.DONE
        self.answers = [None] * (len(ReportStage)-1)
    
    def GetAnswers(self):
        return self.answers
    
    def GetPrompt(self):
        return self.reportPrompt
    
    def RegisterAnswer(self, answer : str):
        self.answers[self.reportStage.value] = answer
    
    def AdvanceStage(self):
        if self.reportStage == ReportStage.IDLE:
            self.reportStage = ReportStage.WHAT_BEFORE
            self.reportPrompt = ReportPrompt.WHAT_BEFORE
        elif self.reportStage == ReportStage.WHAT_BEFORE:
            self.reportStage = ReportStage.DIFFICULTIES
            self.reportPrompt = ReportPrompt.DIFFICULTIES
        elif self.reportStage == ReportStage.DIFFICULTIES:
            self.reportStage = ReportStage.DELAYS
            self.reportPrompt = ReportPrompt.DELAYS
        elif self.reportStage == ReportStage.DELAYS:
            self.reportStage = ReportStage.WHAT_NEXT
            self.reportPrompt = ReportPrompt.WHAT_NEXT
        elif self.reportStage == ReportStage.WHAT_NEXT:
            self.reportStage = ReportStage.DONE
            self.reportPrompt = ReportPrompt.DONE
        elif self.reportStage == ReportStage.DONE:
            self.reportStage = ReportStage.IDLE
            self.reportPrompt = ReportPrompt.IDLE
    
    def ResetStage(self):
        self.reportStage = ReportStage.IDLE
        self.reportPrompt = ReportPrompt.IDLE