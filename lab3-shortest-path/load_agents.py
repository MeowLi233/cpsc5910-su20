# -*- coding: utf-8 -*-

AGENTS = [# ("venv/agents/v1agent.py",  "V1Agent"),
          ("venv/agents/search1agent.py",  "Search1Agent")
         ]

def agents():
    return AGENTS

def agent_names():
    return list(map(lambda p: p[1]), AGENTS)

def file_for(agent_name):
    for p in AGENTS:
        if p[1] == agent_name:
            return p[0]
    return None

