from typing import List, Dict

import CommunicationStructure


class Problem:
    """A DCOP representation

    A DCOP is a Constraints Optimization Problem distribution on a set of
    agents: agents send messages to each other to find a solution to the
    optimization problem.
    A DCOP is traditionally represented as a tuple (V, D, C, A, \mu) where A
    is a set of variables, D the set of the domain for these variables, C a set
    of constraints involving these variables, A a set of agents responsible
    for selecting the value of the variable and \mu is a mapping of the
    variable to the agents.
    Given these elements, the goal is to find an assignment of values to
    variables that minimizes the sum of the costs from the constants.
    """

    def __init__(self, allId: List[int], domains: Dict[int, List[int]],
                 constraintCost: Dict[int, Dict[int, List[List[int]]]],
                 CommunicationStructures: Dict[int, CommunicationStructure], neighbours: Dict[int, List[int]]):
        self.allId = allId
        self.domains = domains
        self.constraintCost = constraintCost
        self.neighbours = neighbours

    def getNeighbourDomain(self, id: int) -> Dict[int, List[int]]:
        neighbourDomain: Dict[int, List[int]] = {}
        neighbour = self.neighbours.get(id)
        for neighbourId in neighbour:
            neighbourDomain[neighbourId] = self.domains.get(neighbourId)
        return neighbourDomain
