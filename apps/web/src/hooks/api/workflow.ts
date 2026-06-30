import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

// Types
export interface Application {
  id: string;
  user_id: string;
  resume_id: string;
  job_id: string;
  company_id?: string;
  status: string;
  stage?: string;
  priority: string;
  probability: number;
  notes?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  application_id: string;
  user_id: string;
  title: string;
  description?: string;
  due_date?: string;
  priority: string;
  status: string;
  task_type: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface TimelineEvent {
  id: string;
  application_id: string;
  event_type: string;
  title: string;
  description?: string;
  event_date: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  application_id?: string;
  notification_type: string;
  title: string;
  message: string;
  priority: string;
  is_read: boolean;
  action_url?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface CompanyProfile {
  id: string;
  user_id: string;
  name: string;
  website?: string;
  industry?: string;
  size?: string;
  location?: string;
  description?: string;
  notes?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface DashboardMetrics {
  total_applications: number;
  applications_by_stage: Record<string, number>;
  pending_tasks: number;
  upcoming_interviews: number;
  unread_notifications: number;
  weekly_progress: Record<string, any>;
  response_rate: number;
  interview_rate: number;
  offer_rate: number;
}

export interface MorningBrief {
  greeting: string;
  today_priorities: Array<{
    title: string;
    priority: string;
    estimated_time: string;
  }>;
  upcoming_interviews: Array<any>;
  deadlines_today: Array<any>;
  recommendations: Array<any>;
  career_health: Record<string, any>;
}

export interface DashboardData {
  metrics: DashboardMetrics;
  morning_brief?: MorningBrief;
  recent_activity: Array<{
    action: string;
    entity_type: string;
    created_at: string;
  }>;
  top_recommendations: Array<any>;
}

export interface KanbanColumn {
  id: string;
  title: string;
  status: string;
  applications: Application[];
}

export interface KanbanBoard {
  columns: KanbanColumn[];
}

// API Hooks
export function useApplications(status?: string) {
  return useQuery({
    queryKey: ['applications', status],
    queryFn: () => apiClient.get<Application[]>(`/api/v1/workflow/applications${status ? `?status=${status}` : ''}`),
  });
}

export function useApplication(applicationId: string) {
  return useQuery({
    queryKey: ['application', applicationId],
    queryFn: () => apiClient.get<Application>(`/api/v1/workflow/applications/${applicationId}`),
    enabled: !!applicationId,
  });
}

export function useCreateApplication() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      resume_id: string;
      job_id: string;
      company_id?: string;
      status?: string;
      priority?: string;
      probability?: number;
      notes?: string;
      metadata?: Record<string, any>;
    }) => apiClient.post<Application>('/api/v1/workflow/applications', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    },
  });
}

export function useUpdateApplication() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ applicationId, data }: {
      applicationId: string;
      data: {
        status?: string;
        priority?: string;
        probability?: number;
        notes?: string;
        metadata?: Record<string, any>;
      };
    }) => apiClient.patch<Application>(`/api/v1/workflow/applications/${applicationId}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    },
  });
}

export function useTasks(applicationId?: string, status?: string) {
  return useQuery({
    queryKey: ['tasks', applicationId, status],
    queryFn: () => apiClient.get<Task[]>(`/api/v1/workflow/tasks${applicationId ? `?application_id=${applicationId}` : ''}${status ? `&status=${status}` : ''}`),
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      application_id: string;
      title: string;
      description?: string;
      due_date?: string;
      priority?: string;
      task_type?: string;
    }) => apiClient.post<Task>('/api/v1/workflow/tasks', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}

export function useUpdateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ taskId, data }: {
      taskId: string;
      data: {
        title?: string;
        description?: string;
        due_date?: string;
        priority?: string;
        status?: string;
      };
    }) => apiClient.patch<Task>(`/api/v1/workflow/tasks/${taskId}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}

export function useTimelineEvents(applicationId: string) {
  return useQuery({
    queryKey: ['timeline', applicationId],
    queryFn: () => apiClient.get<TimelineEvent[]>(`/api/v1/workflow/applications/${applicationId}/timeline`),
    enabled: !!applicationId,
  });
}

export function useCreateTimelineEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      application_id: string;
      event_type: string;
      title: string;
      description?: string;
      event_date?: string;
      metadata?: Record<string, any>;
    }) => apiClient.post<TimelineEvent>(`/api/v1/workflow/applications/${data.application_id}/timeline`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timeline'] });
    },
  });
}

export function useNotifications(unreadOnly: boolean = false) {
  return useQuery({
    queryKey: ['notifications', unreadOnly],
    queryFn: () => apiClient.get<Notification[]>(`/api/v1/workflow/notifications${unreadOnly ? '?unread_only=true' : ''}`),
  });
}

export function useMarkNotificationRead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (notificationId: string) => apiClient.patch<Notification>(`/api/v1/workflow/notifications/${notificationId}/read`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });
}

export function useCompanyProfiles() {
  return useQuery({
    queryKey: ['companies'],
    queryFn: () => apiClient.get<CompanyProfile[]>('/api/v1/workflow/companies'),
  });
}

export function useCreateCompanyProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      name: string;
      website?: string;
      industry?: string;
      size?: string;
      location?: string;
      description?: string;
    }) => apiClient.post<CompanyProfile>('/api/v1/workflow/companies', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['companies'] });
    },
  });
}

export function useDashboard() {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: () => apiClient.get<DashboardData>('/api/v1/workflow/dashboard'),
  });
}

export function useMorningBrief() {
  return useQuery({
    queryKey: ['morning-brief'],
    queryFn: () => apiClient.get<MorningBrief>('/api/v1/workflow/dashboard/morning-brief'),
  });
}

export function useKanbanBoard() {
  return useQuery({
    queryKey: ['kanban'],
    queryFn: () => apiClient.get<KanbanBoard>('/api/v1/workflow/kanban'),
  });
}

export function useTriggerWorkflow() {
  return useMutation({
    mutationFn: (data: {
      event_type: string;
      context: Record<string, any>;
    }) => apiClient.post('/api/v1/workflow/workflow/trigger', data),
  });
}

export function useAnalyzeAutomation() {
  return useMutation({
    mutationFn: (data: {
      applications: Array<any>;
      tasks: Array<any>;
      job_matches: Array<any>;
      skills: string[];
      job_requirements: Array<any>;
      last_activity_date?: string;
      interviews: Array<any>;
      career_health: Record<string, any>;
    }) => apiClient.post('/api/v1/workflow/automation/analyze', data),
  });
}
