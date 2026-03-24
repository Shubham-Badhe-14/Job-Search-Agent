import unittest
import json
from backend.utils.validator import validate_resume_optimization

class TestResumeOptimization(unittest.TestCase):
    def setUp(self):
        self.sample_resume = {
            "skills": ["Python", "Machine Learning"],
            "experience": [
                {
                    "company": "TechCorp",
                    "tools": ["Flask"],
                    "description": ["Improved performance by 20%"]
                }
            ],
            "projects": []
        }

    def test_json_structure(self):
        invalid_json = "Not a JSON"
        is_valid, msg = validate_resume_optimization(self.sample_resume, invalid_json)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Invalid JSON format")

    def test_no_fabricated_metrics(self):
        # Original resume has 20%
        # Optimized has 50% (fabricated)
        optimized_data = {
            "summary": {"overall_alignment_score_estimate": 80},
            "rewrite_suggestions": [
                {"improved_text": "Improved performance by 50% using complex algorithms."}
            ],
            "missing_critical_skills": [],
            "ethics_validation": {"metrics_fabricated": False, "fabrication_detected": False}
        }
        is_valid, msg = validate_resume_optimization(self.sample_resume, json.dumps(optimized_data))
        self.assertFalse(is_valid)
        self.assertIn("Fabricated metrics detected", msg)

    def test_confidence_threshold_low_alignment(self):
        # Alignment score < 40
        optimized_data = {
            "summary": {"overall_alignment_score_estimate": 30},
            "rewrite_suggestions": [],
            "missing_critical_skills": [{"skill": "Docker", "note": "Missing"}],
            "ethics_validation": {"metrics_fabricated": False, "fabrication_detected": False}
        }
        is_valid, data = validate_resume_optimization(self.sample_resume, json.dumps(optimized_data))
        self.assertTrue(is_valid)
        self.assertIn("warning", data["summary"])
        self.assertIn("alignment with this role is currently low", data["summary"]["warning"].lower())

    def test_schema_validation(self):
        # Missing required key 'summary'
        optimized_data = {
            "rewrite_suggestions": [],
            "missing_critical_skills": [],
            "ethics_validation": {}
        }
        is_valid, msg = validate_resume_optimization(self.sample_resume, json.dumps(optimized_data))
        self.assertFalse(is_valid)
        self.assertIn("Missing required key: summary", msg)

if __name__ == '__main__':
    unittest.main()
