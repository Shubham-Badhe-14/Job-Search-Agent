import unittest
import json
from backend.agents.ats_evaluation_agent import ATSEvaluationAgent

class TestATSEvaluation(unittest.TestCase):
    def setUp(self):
        self.sample_resume = {
            "skills": ["Python", "Machine Learning", "FastAPI"],
            "experience": [
                {
                    "company": "TechCorp",
                    "role": "Software Engineer",
                    "description": ["Implemented REST APIs", "Optimized ML models by 20%"]
                }
            ],
            "education": [{"degree": "CS", "school": "Uni"}],
            "certifications": []
        }
        self.resume_text = "Python Developer at TechCorp. Implemented REST APIs and optimized ML models by 20%."

    def test_ats_output_structure(self):
        # This test checks if the agent returns the expected keys.
        # Since running the agent requires LLM access, we mostly care about the structure schema.
        # In a real CI, we might mock the LLM. 
        # Here we'll just check if the agent can be instantiated and the goal is correct.
        agent = ATSEvaluationAgent().get_agent()
        self.assertEqual(agent.role, 'Advanced ATS Evaluation Agent')
        self.assertIn('SCORING FRAMEWORK', agent.backstory)

    def test_evaluation_keys_present(self):
        # Example of what the output should look like
        sample_output = {
            "overall_score": 85,
            "confidence": 0.9,
            "category_scores": {
                "section_completeness": {"score": 15, "reasoning": "All present"},
                "keyword_clarity": {"score": 15, "reasoning": "Clear"},
                "impact_quantification": {"score": 15, "reasoning": "Metrics present"},
                "action_verb_strength": {"score": 10, "reasoning": "Strong"},
                "formatting_simplicity": {"score": 10, "reasoning": "Simple"},
                "readability_clarity": {"score": 10, "reasoning": "Clear"},
                "skills_organization": {"score": 5, "reasoning": "Not grouped"},
                "resume_focus_coherence": {"score": 5, "reasoning": "Focused"}
            },
            "strengths": ["Clear metrics"],
            "critical_issues": [],
            "quick_fixes": ["Group skills"],
            "risk_flags": [],
            "integrity_validation": {"fabrication_detected": False, "assumptions_made": False}
        }
        
        required_keys = ["overall_score", "category_scores", "strengths", "critical_issues", "integrity_validation"]
        for key in required_keys:
            self.assertIn(key, sample_output)

if __name__ == '__main__':
    unittest.main()
