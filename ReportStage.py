from enum import Enum
from strenum import StrEnum

class ReportStage(Enum):
    IDLE = 0
    WHAT_BEFORE = 1
    DIFFICULTIES = 2
    DELAYS = 3
    WHAT_NEXT = 4
    DONE = 5
    
class ReportPrompt(StrEnum):
    IDLE = "Ciao giovine! Facciamo partire il report settimanale?"
    WHAT_BEFORE = "Come và? Di cosa ti sei occupato questa settimana?"
    DIFFICULTIES = "Hai avuto difficoltà particolari?"
    DELAYS = "Ci sono ritardi?"
    WHAT_NEXT = "Cosa farai la prossima settimana?"
    DONE = "Grazie giovine! Alla settimana prossima..."