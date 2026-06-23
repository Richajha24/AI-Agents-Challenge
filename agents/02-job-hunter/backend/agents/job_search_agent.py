from typing import Dict, Any
from .base_agent import BaseAgent


class JobSearchAgent(BaseAgent):
    """Agent for discovering and evaluating relevant job opportunities"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze job market and find relevant opportunities
        
        Args:
            input_data: Contains job_title, skills, experience, location
            
        Returns:
            Dict with relevant jobs, salary estimates, market demand, top companies, opportunity score
        """
        job_title = input_data.get("job_title")
        skills = input_data.get("skills")
        experience = input_data.get("experience")
        location = input_data.get("location")
        
        prompt = f"""
        You are a career strategist and job market analyst. Analyze the job market for the following profile:
        
        Job Title: {job_title}
        Skills: {skills}
        Experience Level: {experience}
        Location: {location}
        
        Provide a comprehensive analysis in the following JSON format:
        {{
            "relevant_jobs": ["list of 5-8 relevant job titles"],
            "salary_estimate": {{
                "min": number,
                "max": number,
                "average": number,
                "currency": "USD"
            }},
            "market_demand": "high/medium/low with explanation",
            "top_hiring_companies": ["list of 5-7 companies"],
            "opportunity_score": number between 0-100,
            "key_requirements": ["list of key requirements for this role"],
            "growth_potential": "description of career growth potential"
        }}
        
        Be realistic and data-driven in your analysis.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert job market analyst and career strategist."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_openai(messages)
        
        # Parse the response (in production, add proper error handling)
        try:
            import json
            result = json.loads(response)
        except:
            result = {
                "relevant_jobs": [job_title],
                "salary_estimate": {"min": 50000, "max": 150000, "average": 100000, "currency": "USD"},
                "market_demand": "medium",
                "top_hiring_companies": ["Tech Corp", "Innovation Inc", "Startup Labs"],
                "opportunity_score": 75,
                "key_requirements": skills.split(","),
                "growth_potential": "Strong growth potential in this field"
            }
        
        return result
