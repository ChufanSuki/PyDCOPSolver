class Parser:
    def __init__(self, rootElement, problem):
        self.rootElement = rootElement
        self.problem = problem
        self.domains = {}
        self.agentNameId = {}
        self.constraintInfo = {}
        self.variableNameAgentId = {}
