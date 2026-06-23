from typing import Dict, Any
from .base_agent import BaseAgent


class InterviewPrepAgent(BaseAgent):
    """Agent for preparing candidates for interviews"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate interview preparation materials
        
        Args:
            input_data: Contains job_description, company_name, resume_content, job_title
            
        Returns:
            Dict with interview questions, technical topics, behavioral questions, STAR answers, prep roadmap
        """
        job_description = input_data.get("job_description", "")
        company_name = input_data.get("company_name", "the company")
        resume_content = input_data.get("resume_content", "")
        job_title = input_data.get("job_title")
        skills = input_data.get("skills", "")
        
        prompt = f"""
        You are an expert interview coach and recruiter. Prepare a comprehensive interview guide for the following:
        
        CANDIDATE PROFILE:
        Resume Summary: {resume_content[:1000] if resume_content else "Not provided"}
        Skills: {skills}
        
        INTERVIEW DETAILS:
        Company: {company_name}
        Position: {job_title}
        Job Description: {job_description}
        
        Create an interview preparation guide in the following JSON format:
        {{
            "interview_questions": [
                {{
                    "question": "specific interview question",
                    "type": "technical/behavioral/situational",
                    "suggested_answer": "brief suggested answer approach"
                }}
            ],
            "technical_topics": [
                {{
                    "topic": "technical area to study",
                    "importance": "high/medium/low",
                    "key_concepts": ["concept 1", "concept 2"]
                }}
            ],
            "behavioral_questions": [
                {{
                    "question": "behavioral question",
                    "star_framework": "Situation, Task, Action, Result approach"
                }}
            ],
            "star_answers": [
                {{
                    "question": "common behavioral question",
                    "star_example": "example STAR answer"
                }}
            ],
            "preparation_roadmap": [
                {{
                    "day": "Day 1-3",
                    "focus": "what to focus on",
                    "tasks": ["task 1", "task 2"]
                }}
            ],
            "company_research_points": ["key things to research about the company"],
            "questions_to_ask": ["questions candidate should ask interviewer"]
        }}
        
        Be specific and practical. Focus on high-impact preparation.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert interview coach and recruiter."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_openai(messages)
        
        try:
            import json
            result = json.loads(response)
        except:
            result = {
                "interview_questions": [
                    {"question": "Tell me about yourself", "type": "behavioral", "suggested_answer": "Focus on relevant experience and achievements"}
                ],
                "technical_topics": [
                    {"topic": "System Design", "importance": "high", "key_concepts": ["Scalability", "Database design"]}
                ],
                "behavioral_questions": [
                    {"question": "Describe a challenging project", "star_framework": "Situation: Describe context, Task: Explain your role, Action: What you did, Result: Outcome"}
                ],
                "star_answers": [
                    {"question": "Tell me about a time you led a team", "star_example": "Situation: Project deadline approaching, Task: Coordinate team efforts, Action: Implemented agile methodology, Result: Delivered on time with high quality"}
                ],
                "preparation_roadmap": [
                    {"day": "Day 1-3", "focus": "Technical fundamentals", "tasks": ["Review core concepts", "Practice coding"]}
                ],
                "company_research_points": ["Recent product launches", "Company culture", "Industry position"],
                "questions_to_ask": ["What does success look like in this role?", "How does the team collaborate?"]
            }
        
        return result
