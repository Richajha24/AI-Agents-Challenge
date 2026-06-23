from typing import Dict, Any
from .base_agent import BaseAgent


class CoverLetterAgent(BaseAgent):
    """Agent for generating personalized cover letters"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized cover letter
        
        Args:
            input_data: Contains resume_content, job_description, company_name
            
        Returns:
            Dict with cover letter content, talking points, personalization suggestions
        """
        resume_content = input_data.get("resume_content")
        job_description = input_data.get("job_description", "")
        company_name = input_data.get("company_name", "the company")
        job_title = input_data.get("job_title")
        
        prompt = f"""
        You are an expert career coach and professional writer. Create a personalized cover letter for the following:
        
        RESUME:
        {resume_content}
        
        JOB DETAILS:
        Company: {company_name}
        Position: {job_title}
        Job Description: {job_description}
        
        Create a compelling cover letter in the following JSON format:
        {{
            "cover_letter": "full cover letter text (300-400 words)",
            "talking_points": [
                "key point 1 to highlight in interviews",
                "key point 2 to highlight in interviews",
                "key point 3 to highlight in interviews"
            ],
            "personalization_suggestions": [
                "suggestion 1 for customizing the letter",
                "suggestion 2 for customizing the letter"
            ],
            "opening_hook": "compelling opening sentence",
            "closing_statement": "strong closing statement"
        }}
        
        Make the cover letter professional, specific, and compelling. Avoid generic phrases.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert career coach and professional writer."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_openai(messages)
        
        try:
            import json
            result = json.loads(response)
        except:
            result = {
                "cover_letter": f"Dear Hiring Manager at {company_name},\n\nI am excited to apply for the {job_title} position. With my background and skills, I am confident in my ability to contribute effectively to your team.\n\n[Customized content based on resume and job requirements]\n\nI look forward to discussing how I can contribute to {company_name}'s success.\n\nSincerely,\n[Your Name]",
                "talking_points": ["Highlight relevant experience", "Show enthusiasm for the company", "Demonstrate problem-solving skills"],
                "personalization_suggestions": ["Research company values", "Mention specific projects", "Reference company news"],
                "opening_hook": "As a passionate professional with experience in...",
                "closing_statement": "I am eager to bring my skills to your team."
            }
        
        return result
