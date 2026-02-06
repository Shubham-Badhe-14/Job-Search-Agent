from unittest.mock import MagicMock
from backend.agents.skill_gap_agent import SkillGapAgent

def test_skill_gap_agent_initialization():
    agent_wrapper = SkillGapAgent()
    agent = agent_wrapper.get_agent()
    assert agent.role == 'Skills Gap Analyst'
    assert agent.goal == 'Compare candidate resume skills against job requirements to identify missing skills'
