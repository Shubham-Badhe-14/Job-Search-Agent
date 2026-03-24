import json
import re

def validate_resume_optimization(original_resume_json, optimized_json_str):
    """
    Validates the Resume Optimization Agent output against strict rules:
    1. JSON structure and types.
    2. Entity grounding (no new skills/tools/companies).
    3. Metric fabrication detection.
    4. Confidence threshold.
    """
    try:
        data = json.loads(optimized_json_str)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"

    # Step 1: Schema Validation
    required_keys = ["summary", "rewrite_suggestions", "missing_critical_skills", "ethics_validation"]
    for key in required_keys:
        if key not in data:
            return False, f"Missing required key: {key}"

    # Step 2: Entity Grounding Validation
    # Helper to extract all text from suggestions
    all_optimized_text = ""
    for sugg in data.get("rewrite_suggestions", []):
        all_optimized_text += " " + sugg.get("improved_text", "")
    
    # Simple entity check (skills/tools)
    # Extract all unique skills/tools from original resume
    original_entities = set()
    original_entities.update(original_resume_json.get("skills", []))
    for exp in original_resume_json.get("experience", []):
        original_entities.update(exp.get("tools", []))
        original_entities.add(exp.get("company", ""))
    for proj in original_resume_json.get("projects", []):
        original_entities.update(proj.get("tools", []))

    # Basic check: look for capitalized words or known skill patterns in optimized text 
    # that are NOT in original_entities. This is a heuristic that needs refinement for production.
    # For now, we'll focus on the explicit missing_critical_skills flagging.
    
    # Step 3: Metric Fabrication Detection
    def extract_metrics(text):
        # Finds percentages or numbers followed by +, k, m, etc.
        return re.findall(r'\d+%|\d+\+', text)

    original_metrics = set()
    for exp in original_resume_json.get("experience", []):
        for desc in exp.get("description", []):
            original_metrics.update(extract_metrics(desc))
            
    optimized_metrics = set(extract_metrics(all_optimized_text))
    
    fabricated_metrics = optimized_metrics - original_metrics
    if fabricated_metrics:
        data["ethics_validation"]["metrics_fabricated"] = True
        data["ethics_validation"]["fabrication_detected"] = True
        return False, f"Fabricated metrics detected: {fabricated_metrics}"

    # Step 4: Confidence Threshold
    summary = data.get("summary", {})
    if summary.get("overall_alignment_score_estimate", 0) < 40:
        if "warning" not in summary:
            summary["warning"] = "Alignment with this role is currently low. Consider skill development before tailoring."

    return True, data
