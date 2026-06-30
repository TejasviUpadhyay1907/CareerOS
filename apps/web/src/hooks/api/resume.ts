/** API hooks for resume operations. */
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/api/v1';

interface UploadResponse {
  id: string;
  original_filename: string;
  storage_url: string;
  file_size: number;
  mime_type: string;
  created_at: string;
}

interface ResumeResponse {
  id: string;
  user_id: string;
  original_filename: string;
  storage_url: string;
  file_size: number;
  mime_type: string;
  is_primary: boolean;
  raw_text?: string;
  parsed_data?: any;
  created_at: string;
  updated_at: string;
}

interface ResumeDetailResponse {
  resume: ResumeResponse;
  metadata?: any;
  analysis?: any;
  skills: any[];
  experience: any[];
  education: any[];
  projects: any[];
  certifications: any[];
  languages: any[];
  achievements: any[];
  links: any[];
}

interface AnalyzeResponse {
  resume_id: string;
  analysis: {
    health_score: number;
    health_breakdown: Record<string, number>;
    recommendations: string[];
    strengths: string[];
    weaknesses: string[];
    missing_sections: string[];
    ats_score?: number;
    formatting_score?: number;
    readability_score?: number;
  };
  metadata: {
    years_of_experience?: number;
    primary_domain?: string;
    career_level?: string;
    total_projects: number;
    total_certifications: number;
    total_achievements: number;
    has_leadership_experience: boolean;
    has_open_source_contributions: boolean;
    has_internships: boolean;
    has_research_experience: boolean;
    has_publications: boolean;
  };
}

interface SummaryResponse {
  professional_summary: string;
  career_highlights: string[];
  top_strengths: string[];
  potential_weaknesses: string[];
  career_level: string;
  primary_technology_stack: string[];
  suggested_job_roles: string[];
  suggested_industries: string[];
  top_keywords: string[];
}

// Upload resume — mutationFn receives a single argument object
export function useUploadResume() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ file, userId }: { file: File; userId: string }) => {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId);

      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume/upload`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error((error as { detail?: string }).detail || 'Upload failed');
      }

      return response.json() as Promise<UploadResponse>;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
    },
  });
}

// List resumes
export function useResumes(userId: string) {
  return useQuery({
    queryKey: ['resumes', userId],
    queryFn: async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume?user_id=${userId}`, {
        headers
      });
      if (!response.ok) {
        throw new Error('Failed to fetch resumes');
      }
      return response.json() as Promise<ResumeResponse[]>;
    },
    enabled: !!userId,
  });
}

// Get resume details
export function useResume(resumeId: string) {
  return useQuery({
    queryKey: ['resume', resumeId],
    queryFn: async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume/${resumeId}`, {
        headers
      });
      if (!response.ok) {
        throw new Error('Failed to fetch resume');
      }
      return response.json() as Promise<ResumeDetailResponse>;
    },
    enabled: !!resumeId,
  });
}

// Analyze resume
export function useAnalyzeResume() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (resumeId: string) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume/analyze`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ resume_id: resumeId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Analysis failed');
      }

      return response.json() as Promise<AnalyzeResponse>;
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['resume', variables] });
    },
  });
}

// Generate summary
export function useGenerateSummary() {
  return useMutation({
    mutationFn: async (resumeId: string) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume/summary`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ resume_id: resumeId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Summary generation failed');
      }

      return response.json() as Promise<SummaryResponse>;
    },
  });
}

// Delete resume
export function useDeleteResume() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (resumeId: string) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('careeros_token') : null;
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/resume/${resumeId}`, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        throw new Error('Failed to delete resume');
      }

      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
    },
  });
}
