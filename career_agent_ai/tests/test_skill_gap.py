import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from career_agent_ai.agents.skill_gap_agent import get_skill_gap_agent

class TestSkillGapAgent(unittest.TestCase):
    
    @patch('career_agent_ai.agents.skill_gap_agent.get_llm')
    def test_agent_initialization(self, mock_get_llm):
        """Test that Skill Gap Agent initializes correctly"""
        mock_get_llm.return_value = MagicMock()
        
        agent = get_skill_gap_agent()
        
        self.assertEqual(agent.role, 'Skill Gap Analyst')
        self.assertIn('Identify missing skills', agent.goal)
        self.assertFalse(agent.allow_delegation)

if __name__ == '__main__':
    unittest.main()
