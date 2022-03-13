from typing import Dict
import xml.etree.ElementTree as ET
from core.agentDescriptor import AgentDescriptor


class AgentParser:
    def __init__(self, agentsPath: str):
        self.agentsPath = agentsPath

    def parse(self) -> Dict[str, AgentDescriptor]:
        map = {}
        try:
            self.tree = ET.parse(self.agentsPath)
            root = self.tree.getroot()
            agents = root.find('./agents')
            for agent in agents:
                name = agent.attrib['name']
                agentDescriptor = AgentDescriptor(agent.attrib['class'], agent.attrib['method'].upper())
                map[name.upper()] = agentDescriptor
        except Exception as e:
            print(e)
        return map
