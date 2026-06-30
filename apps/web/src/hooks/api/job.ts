import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/api/v1';

// Types
export interface JobAnalyzeRequest {
  job_description: string;
  resume_id: string;
}

export interface JobResponse {
  id: string;
  user_id: string;
  title: string;
  company_name: string;
  department?: string;
  employment_type?: string;
  location?: string;
  remote_status?: string;
  experience_required?: string;
  education_required?: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  industry?: string;
  domain?: string;
  seniority?: string;
  raw_description: string;
  parsed_data?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface JobSkill {
  name: string;
  category: string;
  type: string;
  importance?: number;
}

export interface JobRequirement {
  requirement: string;
  category?: string;
  is_mandatory: boolean;
}

export interface JobResponsibility {
  responsibility: string;
  priority?: number;
}

export interface JobBenefit {
  benefit: string;
  category?: string;
}

export interface JobAnalysis {
  hiring_signals: string[];
  urgency: string;
  leadership_required: boolean;
  communication_level: string;
  team_size?: string;
  growth_potential: string;
  work_life_balance: string;
  company_culture_indicators: string[];
  hidden_expectations: string[];
}

export interface JobDetail {
  job: JobResponse;
  skills: JobSkill[];
  requirements: JobRequirement[];
  responsibilities: JobResponsibility[];
  benefits: JobBenefit[];
  analysis?: JobAnalysis;
}

export interface MatchReasoning {
  technical: string;
  experience: string;
  education: string;
  project: string;
  keyword: string;
  ats: string;
  leadership: string;
  communication: string;
  industry: string;
}

export interface ResumeJobMatch {
  id: string;
  job_id: string;
  resume_id: string;
  overall_match: number;
  technical_match: number;
  experience_match: number;
  education_match: number;
  project_match: number;
  keyword_match: number;
  ats_match: number;
  leadership_match: number;
  communication_match: number;
  industry_match: number;
  confidence_score: number;
  match_reasoning: MatchReasoning;
  created_at: string;
}

export interface MissingSkill {
  skill_name: string;
  category: string;
  learning_priority: string;
  estimated_learning_time?: string;
  difficulty?: string;
  free_resources: string[];
}

export interface ATSAnalysis {
  keyword_coverage: number;
  formatting_compatibility: number;
  action_verbs_score: number;
  role_alignment: number;
  missing_keywords: string[];
  resume_length_score: number;
  section_completeness: number;
  optimization_potential: number;
  detailed_report: Record<string, any>;
}

export interface Insights {
  top_strengths: string[];
  biggest_weaknesses: string[];
  reasons_recruiter_may_reject: string[];
  reasons_recruiter_may_shortlist: string[];
  hidden_expectations: string[];
  resume_gaps: string[];
  experience_gaps: string[];
  suggested_resume_changes: string[];
  suggested_projects: string[];
  suggested_certifications: string[];
  suggested_technologies: string[];
  suggested_interview_topics: string[];
}

export interface JobAnalyzeResponse {
  job: JobDetail;
  match: ResumeJobMatch;
  missing_skills: MissingSkill[];
  ats_analysis: ATSAnalysis;
  insights: Insights;
}

// Helper: get auth token
function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('careeros_token');
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// API Functions
async function analyzeJob(request: JobAnalyzeRequest): Promise<JobAnalyzeResponse> {
  const response = await fetch(`${API_BASE}/jobs/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({})) as { detail?: string };
    throw new Error(err.detail || 'Failed to analyze job');
  }

  return response.json();
}

async function getJobs(): Promise<JobResponse[]> {
  const response = await fetch(`${API_BASE}/jobs`, { headers: authHeaders() });
  if (!response.ok) throw new Error('Failed to fetch jobs');
  return response.json();
}

async function getJob(jobId: string): Promise<JobDetail> {
  const response = await fetch(`${API_BASE}/jobs/${jobId}`, { headers: authHeaders() });
  if (!response.ok) throw new Error('Failed to fetch job');
  return response.json();
}

async function deleteJob(jobId: string): Promise<void> {
  const response = await fetch(`${API_BASE}/jobs/${jobId}`, {
    method: 'DELETE',
    headers: authHeaders(),
  });
  if (!response.ok) throw new Error('Failed to delete job');
}

// Hooks
export function useAnalyzeJob() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: analyzeJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });
}

export function useJobs() {
  return useQuery({
    queryKey: ['jobs'],
    queryFn: getJobs,
  });
}

export function useJob(jobId: string) {
  return useQuery({
    queryKey: ['job', jobId],
    queryFn: () => getJob(jobId),
    enabled: !!jobId,
  });
}

export function useDeleteJob() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });
}
