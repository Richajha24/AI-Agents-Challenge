const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface JobSearchRequest {
  job_title: string;
  skills: string;
  experience: string;
  location: string;
}

export interface JobSearchResponse {
  id: number;
  job_title: string;
  skills: string;
  experience: string;
  location: string;
  status: string;
  created_at: string;
}

export interface ResumeUploadRequest {
  resume_content: string;
}

export interface ResumeAnalysisResponse {
  id: number;
  match_score?: number;
  missing_keywords?: string;
  strengths?: string;
  weaknesses?: string;
  ats_suggestions?: string;
}

export async function createJobSearch(data: JobSearchRequest): Promise<JobSearchResponse> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to create job search');
  return response.json();
}

export async function uploadResume(searchId: number, resumeContent: string): Promise<ResumeAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/search/${searchId}/resume`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_content: resumeContent }),
  });
  if (!response.ok) throw new Error('Failed to upload resume');
  return response.json();
}

export async function getSkillGaps(searchId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/search/${searchId}/skill-gaps`);
  if (!response.ok) throw new Error('Failed to get skill gaps');
  return response.json();
}

export async function getCoverLetter(searchId: number, companyName: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/search/${searchId}/cover-letter?company_name=${encodeURIComponent(companyName)}`);
  if (!response.ok) throw new Error('Failed to get cover letter');
  return response.json();
}

export async function getInterviewPrep(searchId: number, companyName: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/search/${searchId}/interview?company_name=${encodeURIComponent(companyName)}`);
  if (!response.ok) throw new Error('Failed to get interview prep');
  return response.json();
}

export async function getCompleteReport(searchId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/search/${searchId}/report`);
  if (!response.ok) throw new Error('Failed to get complete report');
  return response.json();
}
