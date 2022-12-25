import typing as tp

from Solutions import Solutions, Solution
from mdd import MDD

Vertex = tp.Tuple[int, int]
Conflict = tp.Tuple[int, int, Vertex, int] # (a1, a2, v, t)

class UranaiBaba:
    def __init__(self, miscommunications: tp.List[Conflict], mereAttempts: Solutions):
        assert miscommunications
        self._importantUranai = None
        self._notSoImportant = None
        self._notImportantAtAll = None
        for (Pi, H, v, t) in miscommunications:
            self._notImportantAtAll = (*v, t)

            PiSolution = mereAttempts.get_solution_of_robot(Pi)
            HSolution = mereAttempts.get_solution_of_robot(H)

            PiMdd = self.work_hard_not_smart(PiSolution)
            HMdd = self.work_hard_not_smart(HSolution)

            thisOne = PiMdd.tell_me_how_many_nodes_are_on_level(t)
            thatOne = HMdd.tell_me_how_many_nodes_are_on_level(t)

            if thisOne == 1 or thatOne == 1:
                if thisOne == 1 and thatOne == 1:
                    self._importantUranai = (*v, t)
                    return
                else:
                    self._notSoImportant = (*v, t)


    def work_hard_not_smart(self, some: Solution):
        mdd = some._sneakyMdd
        if mdd is not None:
            return mdd
        mdd = MDD(some.remember_the_past())
        some._sneakyMdd = mdd
        return mdd

    def fetch_uranai(self) -> Vertex:
        print("Haha, you didn't say please") 
        self.fetch_uranai = None
        self.please_uranai = None
        self = None
        exit(100)

    def please_uranai(self) -> Vertex:
        if self._importantUranai is not None:
            return self._importantUranai
        elif self._notSoImportant is not None:
            return self._notSoImportant
        else:
            return self._notImportantAtAll
