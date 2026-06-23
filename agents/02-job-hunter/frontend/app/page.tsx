'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Briefcase, FileText, Target, BookOpen, Mail, MessageSquare, Sparkles } from 'lucide-react';
import { createJobSearch, uploadResume, getSkillGaps, getCoverLetter, getInterviewPrep } from '@/lib/api';

export default function Home() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [searchId, setSearchId] = useState<number | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    job_title: '',
    skills: '',
    experience: '',
    location: '',
    resume_content: '',
    company_name: '',
  });

  // Results state
  const [results, setResults] = useState({
    resumeAnalysis: null as any,
    skillGaps: null as any,
    coverLetter: null as any,
    interviewPrep: null as any,
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleJobSearch = async () => {
    setLoading(true);
    try {
      const response = await createJobSearch(formData);
      setSearchId(response.id);
      setStep(2);
    } catch (error) {
      console.error('Error creating job search:', error);
      alert('Failed to create job search. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResumeUpload = async () => {
    if (!searchId) return;
    setLoading(true);
    try {
      const analysis = await uploadResume(searchId, formData.resume_content);
      setResults(prev => ({ ...prev, resumeAnalysis: analysis }));
      setStep(3);
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSkillAnalysis = async () => {
    if (!searchId) return;
    setLoading(true);
    try {
      const gaps = await getSkillGaps(searchId);
      setResults(prev => ({ ...prev, skillGaps: gaps }));
      setStep(4);
    } catch (error) {
      console.error('Error analyzing skills:', error);
      alert('Failed to analyze skill gaps. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCoverLetter = async () => {
    if (!searchId) return;
    setLoading(true);
    try {
      const letter = await getCoverLetter(searchId, formData.company_name || 'Target Company');
      setResults(prev => ({ ...prev, coverLetter: letter }));
      setStep(5);
    } catch (error) {
      console.error('Error generating cover letter:', error);
      alert('Failed to generate cover letter. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleInterviewPrep = async () => {
    if (!searchId) return;
    setLoading(true);
    try {
      const prep = await getInterviewPrep(searchId, formData.company_name || 'Target Company');
      setResults(prev => ({ ...prev, interviewPrep: prep }));
      setStep(6);
    } catch (error) {
      console.error('Error generating interview prep:', error);
      alert('Failed to generate interview prep. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getProgress = () => {
    switch (step) {
      case 1: return 16;
      case 2: return 32;
      case 3: return 48;
      case 4: return 64;
      case 5: return 80;
      case 6: return 100;
      default: return 0;
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-ivory-50 via-white to-forest-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-10 h-10 text-forest-600" />
            <h1 className="text-5xl font-bold font-heading text-graphite-900">
              Job Hunter
            </h1>
          </div>
          <p className="text-xl text-graphite-600 max-w-2xl mx-auto">
            AI-Powered Career Acceleration Platform
          </p>
          <p className="text-sm text-graphite-500 mt-2">
            Maximize your hiring probability with intelligent career strategy
          </p>
        </div>

        {/* Progress Bar */}
        {step > 0 && step < 7 && (
          <div className="mb-8">
            <div className="flex justify-between text-sm text-graphite-600 mb-2">
              <span>Progress</span>
              <span>{getProgress()}%</span>
            </div>
            <Progress value={getProgress()} className="h-2" />
          </div>
        )}

        {/* Main Content */}
        <Tabs value={`step-${step}`} className="w-full">
          <TabsList className="grid w-full grid-cols-6 mb-8">
            <TabsTrigger value="step-1" onClick={() => setStep(1)}>
              <Briefcase className="w-4 h-4 mr-2" />
              Job
            </TabsTrigger>
            <TabsTrigger value="step-2" onClick={() => setStep(2)} disabled={!searchId}>
              <FileText className="w-4 h-4 mr-2" />
              Resume
            </TabsTrigger>
            <TabsTrigger value="step-3" onClick={() => setStep(3)} disabled={!results.resumeAnalysis}>
              <Target className="w-4 h-4 mr-2" />
              Match
            </TabsTrigger>
            <TabsTrigger value="step-4" onClick={() => setStep(4)} disabled={!results.skillGaps}>
              <BookOpen className="w-4 h-4 mr-2" />
              Skills
            </TabsTrigger>
            <TabsTrigger value="step-5" onClick={() => setStep(5)} disabled={!results.coverLetter}>
              <Mail className="w-4 h-4 mr-2" />
              Cover
            </TabsTrigger>
            <TabsTrigger value="step-6" onClick={() => setStep(6)} disabled={!results.interviewPrep}>
              <MessageSquare className="w-4 h-4 mr-2" />
              Interview
            </TabsTrigger>
          </TabsList>

          {/* Step 1: Job Search */}
          <TabsContent value="step-1">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Tell us about your target role
                </CardTitle>
                <CardDescription>
                  Enter your job preferences to get started with personalized career analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-graphite-700 mb-2 block">
                    Target Job Title
                  </label>
                  <Input
                    placeholder="e.g., Senior Software Engineer"
                    value={formData.job_title}
                    onChange={(e) => handleInputChange('job_title', e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-graphite-700 mb-2 block">
                    Your Skills (comma-separated)
                  </label>
                  <Input
                    placeholder="e.g., Python, React, Machine Learning"
                    value={formData.skills}
                    onChange={(e) => handleInputChange('skills', e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-graphite-700 mb-2 block">
                    Experience Level
                  </label>
                  <Input
                    placeholder="e.g., 3-5 years, Senior, Mid-level"
                    value={formData.experience}
                    onChange={(e) => handleInputChange('experience', e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-graphite-700 mb-2 block">
                    Preferred Location
                  </label>
                  <Input
                    placeholder="e.g., San Francisco, Remote"
                    value={formData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                  />
                </div>
                <Button
                  onClick={handleJobSearch}
                  disabled={loading || !formData.job_title || !formData.skills}
                  className="w-full bg-forest-600 hover:bg-forest-700"
                >
                  {loading ? 'Analyzing...' : 'Continue to Resume Upload'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Step 2: Resume Upload */}
          <TabsContent value="step-2">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Upload Your Resume
                </CardTitle>
                <CardDescription>
                  Paste your resume content for AI-powered analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste your resume content here..."
                  value={formData.resume_content}
                  onChange={(e) => handleInputChange('resume_content', e.target.value)}
                  className="min-h-[300px]"
                />
                <Button
                  onClick={handleResumeUpload}
                  disabled={loading || !formData.resume_content}
                  className="w-full bg-forest-600 hover:bg-forest-700"
                >
                  {loading ? 'Analyzing Resume...' : 'Analyze Resume'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Step 3: Resume Analysis Results */}
          <TabsContent value="step-3">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Resume Analysis Results
                </CardTitle>
                <CardDescription>
                  Your resume match analysis and ATS optimization suggestions
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {results.resumeAnalysis && (
                  <>
                    <div className="bg-ivory-50 p-6 rounded-lg">
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">
                        Match Score
                      </h3>
                      <div className="flex items-center gap-4">
                        <Progress value={results.resumeAnalysis.match_score || 0} className="flex-1" />
                        <span className="text-2xl font-bold text-forest-600">
                          {results.resumeAnalysis.match_score || 0}%
                        </span>
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Strengths</h3>
                      <p className="text-graphite-600">
                        {results.resumeAnalysis.strengths || 'No strengths identified'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Areas for Improvement</h3>
                      <p className="text-graphite-600">
                        {results.resumeAnalysis.weaknesses || 'No weaknesses identified'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Missing Keywords</h3>
                      <p className="text-graphite-600">
                        {results.resumeAnalysis.missing_keywords || 'No missing keywords identified'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">ATS Optimization Suggestions</h3>
                      <p className="text-graphite-600">
                        {results.resumeAnalysis.ats_suggestions || 'No suggestions available'}
                      </p>
                    </div>

                    <Button
                      onClick={handleSkillAnalysis}
                      disabled={loading}
                      className="w-full bg-forest-600 hover:bg-forest-700"
                    >
                      {loading ? 'Analyzing Skills...' : 'Analyze Skill Gaps'}
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Step 4: Skill Gaps */}
          <TabsContent value="step-4">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Skill Gap Analysis
                </CardTitle>
                <CardDescription>
                  Identify missing skills and get personalized learning recommendations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {results.skillGaps && (
                  <>
                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Missing Skills</h3>
                      <p className="text-graphite-600">
                        {results.skillGaps.missing_skills || 'No missing skills identified'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Learning Roadmap</h3>
                      <p className="text-graphite-600">
                        {results.skillGaps.learning_roadmap || 'No roadmap available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Recommended Certifications</h3>
                      <p className="text-graphite-600">
                        {results.skillGaps.recommended_certifications || 'No certifications recommended'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Skill Priority</h3>
                      <p className="text-graphite-600">
                        {results.skillGaps.skill_priority || 'No priority information available'}
                      </p>
                    </div>

                    <div className="space-y-2">
                      <label className="text-sm font-medium text-graphite-700 mb-2 block">
                        Target Company Name (for cover letter)
                      </label>
                      <Input
                        placeholder="e.g., Google, Microsoft"
                        value={formData.company_name}
                        onChange={(e) => handleInputChange('company_name', e.target.value)}
                      />
                    </div>

                    <Button
                      onClick={handleCoverLetter}
                      disabled={loading}
                      className="w-full bg-forest-600 hover:bg-forest-700"
                    >
                      {loading ? 'Generating...' : 'Generate Cover Letter'}
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Step 5: Cover Letter */}
          <TabsContent value="step-5">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Your Personalized Cover Letter
                </CardTitle>
                <CardDescription>
                  AI-generated cover letter tailored to your target company
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {results.coverLetter && (
                  <>
                    <div className="bg-ivory-50 p-6 rounded-lg">
                      <h3 className="font-semibold text-lg text-graphite-800 mb-4">Cover Letter</h3>
                      <p className="text-graphite-700 whitespace-pre-wrap">
                        {results.coverLetter.cover_letter_content || 'No cover letter generated'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Key Talking Points</h3>
                      <p className="text-graphite-600">
                        {results.coverLetter.talking_points || 'No talking points available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Personalization Suggestions</h3>
                      <p className="text-graphite-600">
                        {results.coverLetter.personalization_suggestions || 'No suggestions available'}
                      </p>
                    </div>

                    <Button
                      onClick={handleInterviewPrep}
                      disabled={loading}
                      className="w-full bg-forest-600 hover:bg-forest-700"
                    >
                      {loading ? 'Generating...' : 'Generate Interview Prep'}
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Step 6: Interview Prep */}
          <TabsContent value="step-6">
            <Card className="border-forest-200">
              <CardHeader>
                <CardTitle className="font-heading text-2xl text-forest-800">
                  Interview Preparation Guide
                </CardTitle>
                <CardDescription>
                  Comprehensive interview preparation materials for your target role
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {results.interviewPrep && (
                  <>
                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Interview Questions</h3>
                      <p className="text-graphite-600">
                        {results.interviewPrep.interview_questions || 'No questions available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Technical Topics to Study</h3>
                      <p className="text-graphite-600">
                        {results.interviewPrep.technical_topics || 'No topics available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Behavioral Questions</h3>
                      <p className="text-graphite-600">
                        {results.interviewPrep.behavioral_questions || 'No questions available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">STAR Framework Answers</h3>
                      <p className="text-graphite-600">
                        {results.interviewPrep.star_answers || 'No STAR answers available'}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-lg text-graphite-800 mb-2">Preparation Roadmap</h3>
                      <p className="text-graphite-600">
                        {results.interviewPrep.preparation_roadmap || 'No roadmap available'}
                      </p>
                    </div>

                    <div className="bg-forest-50 p-6 rounded-lg border border-forest-200">
                      <h3 className="font-semibold text-lg text-forest-800 mb-2">
                        🎉 Analysis Complete!
                      </h3>
                      <p className="text-forest-700">
                        You now have a comprehensive career strategy including resume analysis,
                        skill gap identification, personalized cover letter, and interview preparation.
                        Good luck with your job search!
                      </p>
                    </div>

                    <Button
                      onClick={() => {
                        setStep(1);
                        setSearchId(null);
                        setResults({
                          resumeAnalysis: null,
                          skillGaps: null,
                          coverLetter: null,
                          interviewPrep: null,
                        });
                        setFormData({
                          job_title: '',
                          skills: '',
                          experience: '',
                          location: '',
                          resume_content: '',
                          company_name: '',
                        });
                      }}
                      className="w-full bg-graphite-600 hover:bg-graphite-700"
                    >
                      Start New Analysis
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
