import xml.etree.ElementTree as ET
import problem


class Parser:
    def __init__(self, root: ET.Element = None, problem: problem.Problem = None):
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
        index = 0
        for agent in agents:
            self.problem.allId[index] = agent.attrib["id"]
            index = index + 1
            self.agentNameId[agent.attrib["name"]] = agent.attrib["id"]

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
            assert ids == 2
            agentPair = self.AgentPair(constraint.attrib["scope"], self.variableNameAgentId[ids[0]],
                                       self.variableNameAgentId[ids[1]])
            self.constraintInfo[constraintName] = agentPair

    class AgentPair:
        def __init__(self, scope: str, former: int, latter: int):
            ids = scope.split(" ")
            if len(ids) != 2:
                print("Illegal Argument")
            else:
                self.former = former
                self.latter = latter

    def processTuple(self, tuple: str, constraintName: str):
        tuples = tuple.split("\\|")
        pair: Parser.AgentPair = self.constraintInfo.get(constraintName)
        formerConstraintCost = [[0 for j in range(len(self.problem.domains[pair.former]))] for i in
                                range(len(self.problem.domains[pair.latter]))]
        latterConstraintCost = [[0 for j in range(len(self.problem.domains[pair.latter]))] for i in range(len(
            self.problem.domains[pair.former]))]
        for t in tuples:
            info = t.split("[:| ]")
            formerValue = int(info[1]) - 1
            latterValue = int(info[2]) - 1
            cost = int(info[0])
            formerConstraintCost[formerValue][latterValue] = cost
            latterConstraintCost[latterValue][formerValue] = cost
        constraintCost = self.problem.constraintCost[pair.former]
        if constraintCost == None:
            constraintCost = {}
            self.problem.constraintCost[pair.former] = constraintCost
            constraintCost[pair.latter] = latterConstraintCost
        constraintCost = self.problem.constraintCost[pair.latter]
        if constraintCost == None:
            constraintCost = {}
            self.problem.constraintCost[pair.latter] = constraintCost
            constraintCost[pair.latter] = latterConstraintCost
        constraintCost = self.problem.constraintCost[pair.former]
