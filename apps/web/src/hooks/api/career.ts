import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

// TypeScript interfaces
export interface HealthBreakdownItem {
  score: number;
  weight: number;
  reasoning: string;
}

export interface HealthScore {
  overall_score: number;
  breakdown: Record<string, HealthBreakdownItem>;
  grade: string;
  trend: string;
}

export interface Insight {
  id: string;
  type: string;
  title: string;
  description: string;
  category: string;
  severity: string;
  confidence: number;
  evidence: string[];
  actionable: boolean;
  created_at: string;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  difficulty: string;
  estimated_time: string;
  expected_benefit: string;
  confidence: number;
  evidence: string[];
  status: string;
  user_status: string;
  completed_at: string | null;
  created_at: string;
}

export interface Prediction {
  id: string;
  type: string;
  title: string;
  description: string;
  predicted_value: number;
  confidence: number;
  time_horizon: string;
  factors: string[];
  created_at: string;
}

export interface Opportunity {
  type: string;
  title: string;
  description: string;
  confidence: number;
  evidence: string[];
}

export interface CareerGoal {
  id: string;
  title: string;
  description: string | null;
  category: string;
  target_date: string | null;
  status: string;
  priority: string;
  progress: number;
  created_at: string;
}

export interface CareerProfile {
  id: string;
  user_id: string;
  current_role: string | null;
  target_role: string | null;
  target_industry: string | null;
  target_seniority: string | null;
  salary_expectation_min: number | null;
  salary_expectation_max: number | null;
  preferred_locations: string[] | null;
  remote_preference: string | null;
  work_style: string | null;
  career_stage: string | null;
  years_experience: number | null;
  primary_domain: string | null;
  secondary_domains: string[] | null;
  career_focus_areas: string[] | null;
  learning_style: string | null;
  risk_tolerance: string | null;
  growth_priority: string | null;
  work_life_balance_priority: string | null;
  company_size_preference: string | null;
  company_type_preference: string | null;
  created_at: string;
  updated_at: string;
}

export interface TodayPriority {
  title: string;
  description: string;
  estimated_time: string;
  expected_benefit: string;
  confidence: number;
}

export interface DashboardData {
  greeting: string;
  health_score: HealthScore;
  todays_priorities: TodayPriority[];
  insights: Insight[];
  recommendations: Recommendation[];
  predictions: Prediction[];
  opportunities: Opportunity[];
  goals: CareerGoal[];
  profile: CareerProfile;
}

// API hooks
export function useCareerDashboard() {
  return useQuery({
    queryKey: ['career', 'dashboard'],
    queryFn: () => apiClient.get<DashboardData>('/api/v1/career/dashboard'),
    staleTime: 5 * 60 * 1000,
  });
}

export function useCareerHealth() {
  return useQuery({
    queryKey: ['career', 'health'],
    queryFn: () => apiClient.get<HealthScore>('/api/v1/career/health'),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUpdateCareerProfile() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (profileData: Partial<CareerProfile>) =>
      apiClient.patch<CareerProfile>('/api/v1/career/profile', profileData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['career'] });
    },
  });
}

export function useCreateCareerGoal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (goalData: {
      title: string;
      description?: string;
      category: string;
      target_date?: string;
      priority: string;
    }) => apiClient.post<{ id: string; message: string }>('/api/v1/career/goals', goalData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['career'] });
    },
  });
}

export function useUpdateRecommendation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      recommendationId,
      feedback,
    }: {
      recommendationId: string;
      feedback: { status: string; user_status: string; feedback?: string };
    }) =>
      apiClient.patch(`/api/v1/career/recommendations/${recommendationId}`, feedback),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['career'] });
    },
  });
}
