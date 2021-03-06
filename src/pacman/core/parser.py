import re
import xml.etree.ElementTree as ET
from pacman.core.problem import Problem


class Parser:
    def __init__(self, root: ET.Element = None, problem: Problem = None):
        self.root = root
        self.problem = problem
        self.domains = {}
        self.agentNameId = {}
        self.constraintInfo = {}
        self.variableNameAgentId = {}

    def parseContent(self):
        self.parseAgents()
        self.parseDomain()
        self.parseVariables()
        self.parseConstraints()

    def parseAgents(self):
        agents = self.root.find("./agents")
        self.problem.allId = [0] * int(agents.attrib["nbAgents"])
        index = 0
        for agent in agents:
            self.problem.allId[index] = int(agent.attrib["id"])
            index = index + 1
            self.agentNameId[agent.attrib["name"]] = int(agent.attrib["id"])

    def parseDomain(self):
        domains = self.root.find("./domains")
        for domain in domains:
            name = domain.attrib["name"]
            domain_value = [0] * int(domain.attrib["nbValues"])
            for i in range(len(domain_value)):
                domain_value[i] = i + 1
            self.domains[name] = domain_value

    def parseVariables(self):
        variables = self.root.find("./variables")
        self.problem.domains = {}
        for variable in variables:
            domain = variable.attrib["domain"]
            agentName = variable.attrib["agent"]
            name = variable.attrib["name"]
            self.variableNameAgentId[name] = self.agentNameId[agentName]
            self.problem.domains[self.agentNameId[agentName]] = self.domains[domain]

    def parseConstraints(self):
        self.problem.constraintCost = {}
        self.problem.neighbours = {}
        constraints = self.root.find("./constraints")
        for constraint in constraints:
            constraintName = constraint.attrib["reference"]
            ids = constraint.attrib["scope"].split(" ")
            assert ids.__len__() == 2
            agentPair = self.AgentPair(constraint.attrib["scope"], self.variableNameAgentId[ids[0]],
                                       self.variableNameAgentId[ids[1]])
            self.constraintInfo[constraintName] = agentPair
        constraintElements = self.root.find("./relations")
        for constraintElement in constraintElements:
            name = constraintElement.attrib["name"]
            self.processTuple(constraintElement.text, name)
        for agentId in self.problem.allId:
            neighbours = self.problem.constraintCost[agentId].keys()
            neighbourArray = [0] * neighbours.__len__()
            index = 0
            for neighbourId in neighbours:
                neighbourArray[index] = neighbourId
                index = index + 1
            self.problem.neighbours[agentId] = neighbourArray

    class AgentPair:
        def __init__(self, scope: str, former: int, latter: int):
            ids = scope.split(" ")
            if len(ids) != 2:
                print("Illegal Argument")
            else:
                self.former = former
                self.latter = latter

    def processTuple(self, tuple: str, constraintName: str):
        """Prcoess tuple to fill in problem.constraintCost

        Arguments:
            tuple {str} -- tuple e.g. 40:1 3|73:2 1|76:1 2|54:3 2|69:3 3|18:2 2|83:1 1|60:3 1|15:2 3
            constraintName {str} -- constraint name e.g. R0

        """

        tuples = re.split("\\|", tuple)
        pair: Parser.AgentPair = self.constraintInfo.get(constraintName)
        formerConstraintCost = [[0 for j in range(len(self.problem.domains[pair.latter]))] for i in
                                range(len(self.problem.domains[pair.former]))]
        latterConstraintCost = [[0 for j in range(len(self.problem.domains[pair.former]))] for i in range(len(
            self.problem.domains[pair.latter]))]
        for t in tuples:
            info = re.split("[:| ]", t)
            formerValue = int(info[1]) - 1
            latterValue = int(info[2]) - 1
            cost = int(info[0])
            formerConstraintCost[formerValue][latterValue] = cost
            latterConstraintCost[latterValue][formerValue] = cost
        if pair.former not in self.problem.constraintCost:
            constraintCost = {}
            self.problem.constraintCost[pair.former] = constraintCost
        else:
            constraintCost = self.problem.constraintCost[pair.former]
        constraintCost[pair.latter] = formerConstraintCost
        if pair.latter not in self.problem.constraintCost:
            constraintCost = {}
            self.problem.constraintCost[pair.latter] = constraintCost
        else:
            constraintCost = self.problem.constraintCost[pair.latter]
        constraintCost[pair.former] = latterConstraintCost
