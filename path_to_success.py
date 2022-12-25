import typing as tp
from enum import Enum, auto

from Solutions import Solutions, Solution
from mdd import MDD

Vertex = tp.Tuple[int, int]
Conflict = tp.Tuple[int, int, Vertex, int] # (a1, a2, v, t)

class ConflictType(Enum):
    cardinal = auto()
    semiCardinal = auto()
    nonCardinal = auto()

    def __init__(self, idx) -> None:
        self.cardinalAgent = idx


class UranaiBaba:
    def __init__(self, miscommunications: tp.List[Conflict], mereAttempts: Solutions):
        assert miscommunications
        self._importantUranai = None
        self._notSoImportant = None
        for miscommunication in miscommunications:
            (Pi, H, v, t) = miscommunication
            self._notImportantAtAll = miscommunication

            PiSolution = mereAttempts.get_solution_of_robot(Pi)
            HSolution = mereAttempts.get_solution_of_robot(H)

            PiMdd = self.work_hard_not_smart(PiSolution)
            HMdd = self.work_hard_not_smart(HSolution)

            thisOne = PiMdd.tell_me_how_many_nodes_are_on_level(t)
            thatOne = HMdd.tell_me_how_many_nodes_are_on_level(t)

            if thisOne == 1 or thatOne == 1:
                if thisOne == 1 and thatOne == 1:
                    self._importantUranai = miscommunication
                    return
                else:
                    self.notFlexible = Pi
                    if thatOne == 1: 
                        # meaning thisOne != 1 and thatOne == 1
                        self.notFlexible = H

                    self._notSoImportant = miscommunication


    def work_hard_not_smart(self, some: Solution):
        mdd = some._sneakyMdd
        if mdd is not None:
            return mdd
        mdd = MDD(some.remember_the_past())
        some._sneakyMdd = mdd
        return mdd

    def fetch_uranai(self) -> Conflict:
        print("Haha, you didn't say please") 
        self.fetch_uranai = None
        self.please_uranai = None
        self = None
        exit(100)

    def please_uranai(self) -> tp.Tuple[Conflict, ConflictType]:
        if self._importantUranai is not None:
            return (self._importantUranai, ConflictType.cardinal)
        elif self._notSoImportant is not None:
            res = ConflictType.semiCardinal
            res.cardinalAgent = self.notFlexible
            return (self._notSoImportant, res)
        else:
            return (self._notImportantAtAll, ConflictType.nonCardinal)
