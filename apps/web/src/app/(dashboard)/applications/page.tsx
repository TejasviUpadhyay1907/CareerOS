'use client';

import { useState } from 'react';
import { Plus, Search, Building2, MapPin, Calendar, ExternalLink, Loader2, X } from 'lucide-react';
import {
  useApplications,
  useCreateApplication,
  useUpdateApplication,
} from '@/hooks/api/workflow';
import { useResumes } from '@/hooks/api/resume';
import { useJobs } from '@/hooks/api/job';
import { useAuth } from '@/components/providers/auth-provider';

const STATUS_COLORS: Record<string, string> = {
  wishlist:    'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
  preparing:   'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300',
  applied:     'bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300',
  oa_received: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300',
  interview:   'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300',
  offer:       'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
  rejected:    'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300',
  accepted:    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300',
};

const ALL_STATUSES = ['wishlist','preparing','applied','oa_received','interview','offer','rejected','accepted'];

export default function ApplicationsPage() {
  const { user } = useAuth();
  const { data: applications = [], isLoading } = useApplications();
  const { data: resumes = [] } = useResumes(user?.id ?? '');
  const { data: jobs = [] } = useJobs();
  const createMutation = useCreateApplication();
  const updateMutation = useUpdateApplication();

  const [search, setSearch] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showAdd, setShowAdd] = useState(false);

  // Add form state
  const [addResumeId, setAddResumeId] = useState('');
  const [addJobId, setAddJobId] = useState('');
  const [addStatus, setAddStatus] = useState('wishlist');
  const [addNotes, setAddNotes] = useState('');
  const [addError, setAddError] = useState('');

  const handleAdd = async () => {
    if (!addResumeId) { setAddError('Select a resume.'); return; }
    // job_id is optional — user can add application without analyzing job first
    setAddError('');
    try {
      await createMutation.mutateAsync({
        resume_id: addResumeId,
        job_id: addJobId || undefined,
        status: addStatus,
        notes: addNotes || undefined,
      });
      setShowAdd(false);
      setAddResumeId(''); setAddJobId(''); setAddStatus('wishlist'); setAddNotes('');
    } catch (err) {
      setAddError(err instanceof Error ? err.message : 'Failed to create application');
    }
  };

  const handleStatusChange = async (appId: string, newStatus: string) => {
    await updateMutation.mutateAsync({ applicationId: appId, data: { status: newStatus } });
  };

  const filtered = applications.filter((app) => {
    const jobMatch = jobs.find((j) => j.id === app.job_id);
    const label = jobMatch
      ? `${jobMatch.title} ${jobMatch.company_name}`
      : (app.job_id ?? app.notes ?? '');
    const matchSearch = label.toLowerCase().includes(search.toLowerCase());
    const matchStatus = filterStatus === 'all' || app.status === filterStatus;
    return matchSearch && matchStatus;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Applications</h1>
          <p className="mt-1 text-muted-foreground">Track and manage your job applications</p>
        </div>
        <button
          onClick={() => setShowAdd(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 text-sm font-medium transition-colors"
        >
          <Plus className="w-4 h-4" /> Add Application
        </button>
      </div>

      {/* Add Application Modal */}
      {showAdd && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-card rounded-2xl p-6 w-full max-w-md border shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Add Application</h2>
              <button onClick={() => setShowAdd(false)}>
                <X className="w-5 h-5 text-muted-foreground" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-1 block">Resume</label>
                {resumes.length === 0 ? (
                  <p className="text-sm text-muted-foreground">Upload a resume first on the Resume page.</p>
                ) : (
                  <select
                    value={addResumeId}
                    onChange={(e) => setAddResumeId(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option value="">— select resume —</option>
                    {resumes.map((r) => (
                      <option key={r.id} value={r.id}>{r.original_filename}</option>
                    ))}
                  </select>
                )}
              </div>

              <div>
                <label className="text-sm font-medium mb-1 block">Job <span className="text-muted-foreground font-normal">(optional)</span></label>
                <select
                  value={addJobId}
                  onChange={(e) => setAddJobId(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">— none / enter manually —</option>
                  {jobs.map((j) => (
                    <option key={j.id} value={j.id}>{j.title} @ {j.company_name}</option>
                  ))}
                </select>
                {jobs.length === 0 && (
                  <p className="text-xs text-muted-foreground mt-1">
                    Tip: Analyze a job on the Job Analysis page to link it here.
                  </p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium mb-1 block">Status</label>
                <select
                  value={addStatus}
                  onChange={(e) => setAddStatus(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  {ALL_STATUSES.map((s) => (
                    <option key={s} value={s}>{s.replace('_', ' ')}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-sm font-medium mb-1 block">Notes (optional)</label>
                <textarea
                  value={addNotes}
                  onChange={(e) => setAddNotes(e.target.value)}
                  rows={3}
                  placeholder="Any notes about this application..."
                  className="w-full px-3 py-2 border rounded-lg bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                />
              </div>

              {addError && (
                <p className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">{addError}</p>
              )}

              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => setShowAdd(false)}
                  className="flex-1 py-2 border rounded-lg text-sm hover:bg-secondary transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAdd}
                  disabled={createMutation.isPending}
                  className="flex-1 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-50 flex items-center justify-center gap-2 transition-colors"
                >
                  {createMutation.isPending && <Loader2 className="w-4 h-4 animate-spin" />}
                  Add Application
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search applications..."
            className="w-full pl-10 pr-4 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
          />
        </div>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
        >
          <option value="all">All Status</option>
          {ALL_STATUSES.map((s) => (
            <option key={s} value={s}>{s.replace('_', ' ')}</option>
          ))}
        </select>
      </div>

      {/* List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-card rounded-xl border">
          <Briefcase className="w-12 h-12 mx-auto text-muted-foreground opacity-30 mb-3" />
          <p className="text-muted-foreground">
            {applications.length === 0
              ? 'No applications yet. Click "Add Application" to track your first one.'
              : 'No applications match your filters.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((app) => {
            const job = jobs.find((j) => j.id === app.job_id);
            return (
              <div key={app.id} className="bg-card rounded-xl p-5 border hover:border-primary/40 transition-colors">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-semibold">{job?.title ?? 'Unknown Role'}</h3>
                      <span className={`px-2 py-0.5 text-xs rounded-full capitalize ${STATUS_COLORS[app.status] ?? ''}`}>
                        {app.status.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 mt-1.5 text-sm text-muted-foreground flex-wrap">
                      {job?.company_name && (
                        <span className="flex items-center gap-1">
                          <Building2 className="w-3.5 h-3.5" />
                          {job.company_name}
                        </span>
                      )}
                      {job?.location && (
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3.5 h-3.5" />
                          {job.location}
                        </span>
                      )}
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5" />
                        {new Date(app.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    {app.notes && (
                      <p className="text-xs text-muted-foreground mt-2 line-clamp-1">{app.notes}</p>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <select
                      value={app.status}
                      onChange={(e) => handleStatusChange(app.id.toString(), e.target.value)}
                      className="text-xs px-2 py-1 border rounded bg-background focus:outline-none"
                    >
                      {ALL_STATUSES.map((s) => (
                        <option key={s} value={s}>{s.replace('_', ' ')}</option>
                      ))}
                    </select>
                    {job && (
                      <a
                        href={`/job-analysis?job_id=${job.id}`}
                        className="flex items-center gap-1 text-xs text-primary hover:underline"
                      >
                        <ExternalLink className="w-3 h-3" /> View Job
                      </a>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function Briefcase({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M21 13.5V19a2 2 0 01-2 2H5a2 2 0 01-2-2v-5.5M21 13.5H3M21 13.5l-2-7H5l-2 7M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2" />
    </svg>
  );
}
