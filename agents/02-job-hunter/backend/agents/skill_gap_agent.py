from typing import Dict, Any
from .base_agent import BaseAgent


class SkillGapAgent(BaseAgent):
    """Agent for identifying missing skills and creating learning roadmaps"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify skill gaps and create learning roadmap
        
        Args:
            input_data: Contains resume_content, target_role, required_skills
            
        Returns:
            Dict with missing skills, learning roadmap, certifications, skill priority
        """
        resume_content = input_data.get("resume_content", "")
        target_role = input_data.get("target_role")
        current_skills = input_data.get("skills", "")
        
        prompt = f"""
        You are a career development expert and learning strategist. Analyze the skill gap for the following profile:
        
        CURRENT PROFILE:
        Skills: {current_skills}
        Resume Summary: {resume_content[:1000] if resume_content else "Not provided"}
        
        TARGET ROLE:
        {target_role}
        
        Provide a comprehensive skill gap analysis in the following JSON format:
        {{
            "missing_skills": ["list of 5-8 missing critical skills"],
            "learning_roadmap": [
                {{
                    "skill": "skill name",
                    "priority": "high/medium/low",
                    "estimated_time": "time to learn",
                    "resources": ["specific learning resources"],
                    "difficulty": "beginner/intermediate/advanced"
                }}
            ],
            "recommended_certifications": [
                {{
                    "name": "certification name",
                    "provider": "certification provider",
                    "value": "why this certification is valuable"
                }}
            ],
            "skill_priority": [
                {{
                    "skill": "skill name",
                    "priority_score": number between 0-100,
                    "impact": "impact on career"
                }}
            ],
            "quick_wins": ["skills that can be learned quickly for high impact"]
        }}
        
        Be practical and prioritize skills that have the highest ROI.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert career development strategist."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_openai(messages)
        
        try:
            import json
            result = json.loads(response)
        except:
            result = {
                "missing_skills": ["Cloud computing", "Machine Learning", "System Design"],
                "learning_roadmap": [
                    {"skill": "Cloud Computing", "priority": "high", "estimated_time": "2-3 months", "resources": ["AWS Certified Solutions Architect"], "difficulty": "intermediate"}
                ],
                "recommended_certifications": [
                    {"name": "AWS Solutions Architect", "provider": "Amazon", "value": "Industry standard for cloud roles"}
                ],
                "skill_priority": [
                    {"skill": "Cloud Computing", "priority_score": 90, "impact": "High demand skill"}
                ],
                "quick_wins": ["API design", "Git workflows"]
            }
        
        return result
