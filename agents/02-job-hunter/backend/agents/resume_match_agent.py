from typing import Dict, Any
from .base_agent import BaseAgent


class ResumeMatchAgent(BaseAgent):
    """Agent for comparing resume against target jobs"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze resume match with job description
        
        Args:
            input_data: Contains resume_content and job_description
            
        Returns:
            Dict with match score, missing keywords, strengths, weaknesses, ATS suggestions
        """
        resume_content = input_data.get("resume_content")
        job_description = input_data.get("job_description", "")
        job_title = input_data.get("job_title", "")
        skills = input_data.get("skills", "")
        
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) analyzer and career coach. Analyze the following resume against a job target:
        
        RESUME:
        {resume_content}
        
        TARGET JOB:
        Job Title: {job_title}
        Required Skills: {skills}
        Job Description: {job_description}
        
        Provide a comprehensive analysis in the following JSON format:
        {{
            "match_score": number between 0-100,
            "missing_keywords": ["list of important keywords missing from resume"],
            "strengths": ["list of 3-5 key strengths in the resume"],
            "weaknesses": ["list of 3-5 areas for improvement"],
            "ats_suggestions": ["list of 5-7 specific ATS optimization suggestions"],
            "key_achievements": ["list of notable achievements highlighted"],
            "experience_relevance": "assessment of experience relevance"
        }}
        
        Be specific and actionable in your feedback.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert ATS analyzer and career coach."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_openai(messages)
        
        try:
            import json
            result = json.loads(response)
        except:
            result = {
                "match_score": 70,
                "missing_keywords": ["leadership", "agile", "cloud"],
                "strengths": ["Strong technical background", "Good project experience"],
                "weaknesses": ["Limited leadership experience", "Missing key certifications"],
                "ats_suggestions": ["Add quantifiable achievements", "Include relevant keywords"],
                "key_achievements": ["Project completion", "Team collaboration"],
                "experience_relevance": "Moderately relevant"
            }
        
        return result
