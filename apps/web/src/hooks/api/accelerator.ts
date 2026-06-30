import { useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

// TypeScript interfaces
export interface ResumeChange {
  original: string;
  optimized: string;
  reason: string;
  ats_improvement: string;
  recruiter_impact: string;
}

export interface SkillsOptimization {
  original_order: string[];
  optimized_order: string[];
  reasoning: string;
}

export interface KeywordAddition {
  keyword: string;
  where_added: string;
  reason: string;
}

export interface ResumeOptimization {
  id: string;
  optimized_summary: string;
  optimized_experience: ResumeChange[];
  optimized_skills: SkillsOptimization;
  optimized_projects: ResumeChange[];
  keyword_additions: KeywordAddition[];
  optimization_score: number;
  estimated_ats_improvement: number;
  estimated_match_increase: number;
  estimated_interview_probability: number;
  created_at: string;
}

export interface PersonalizationPoint {
  point: string;
  source: string;
}

export interface CoverLetter {
  id: string;
  content: string;
  tone: string;
  length: string;
  company_name: string;
  role_title: string;
  personalization_points: PersonalizationPoint[];
  created_at: string;
}

export interface RecruiterMessage {
  id: string;
  message_type: string;
  subject: string | null;
  content: string;
  tone: string;
  length: string;
  personalization_reason: string;
  call_to_action: string;
  recipient_name: string | null;
  recipient_company: string | null;
  platform: string;
  created_at: string;
}

export interface TechnicalTopic {
  topic: string;
  priority: string;
  resources: string[];
}

export interface BehavioralQuestion {
  question: string;
  star_suggestion: string;
  priority: string;
}

export interface ProjectQuestion {
  question: string;
  suggested_answer: string;
  priority: string;
}

export interface CodingTopic {
  topic: string;
  priority: string;
  practice_problems: string[];
}

export interface SystemDesignTopic {
  topic: string;
  priority: string;
  key_concepts: string[];
}

export interface QuestionToAsk {
  question: string;
  reason: string;
}

export interface StudyPlanItem {
  time: string | null;
  task: string;
  priority: string;
}

export interface StudyPlanDay {
  day: string;
  tasks: string[];
  focus: string;
}

export interface PriorityRanking {
  highest_priority: string[];
  high_priority: string[];
  medium_priority: string[];
  low_priority: string[];
}

export interface InterviewKit {
  id: string;
  company_name: string;
  role_title: string;
  company_overview: string;
  role_overview: string;
  responsibilities: string[];
  technical_topics: TechnicalTopic[];
  behavioral_questions: BehavioralQuestion[];
  project_questions: ProjectQuestion[];
  resume_questions: ProjectQuestion[];
  coding_topics: CodingTopic[];
  system_design_topics: SystemDesignTopic[];
  hr_questions: { question: string; suggested_answer: string }[];
  salary_tips: string[];
  questions_to_ask: QuestionToAsk[];
  study_plan_90min: StudyPlanItem[];
  study_plan_3day: StudyPlanDay[];
  study_plan_7day: StudyPlanDay[];
  priority_ranking: PriorityRanking;
  created_at: string;
}

// API hooks
export function useOptimizeResume() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { resume_id: string; job_id: string }) =>
      apiClient.post<ResumeOptimization>('/api/v1/accelerator/optimize/resume', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accelerator'] });
    },
  });
}

export function useGenerateCoverLetter() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { resume_id: string; job_id: string; tone?: string; length?: string }) =>
      apiClient.post<CoverLetter>('/api/v1/accelerator/cover-letter/generate', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accelerator'] });
    },
  });
}

export function useGenerateOutreach() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: {
      resume_id: string;
      job_id?: string;
      message_type?: string;
      tone?: string;
      length?: string;
    }) => apiClient.post<RecruiterMessage>('/api/v1/accelerator/outreach/generate', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accelerator'] });
    },
  });
}

export function useGenerateInterviewKit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { resume_id: string; job_id: string }) =>
      apiClient.post<InterviewKit>('/api/v1/accelerator/interview/generate', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accelerator'] });
    },
  });
}

export function useExportDocument() {
  return useMutation({
    mutationFn: (data: { document_id: string; format?: string }) =>
      apiClient.post<{ file_path: string; format: string; file_size: number }>(
        '/api/v1/accelerator/documents/export',
        data
      ),
  });
}
