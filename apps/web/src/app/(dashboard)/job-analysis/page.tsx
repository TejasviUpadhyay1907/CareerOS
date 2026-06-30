'use client';

import { useState } from 'react';
import { Search, CheckCircle, AlertCircle, Target, Loader2 } from 'lucide-react';
import { useAnalyzeJob } from '@/hooks/api/job';
import { useResumes } from '@/hooks/api/resume';
import { useAuth } from '@/components/providers/auth-provider';

export default function JobAnalysisPage() {
  const { user } = useAuth();
  const [jobDescription, setJobDescription] = useState('');
  const [selectedResumeId, setSelectedResumeId] = useState('');
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState('');

  const { data: resumes = [] } = useResumes(user?.id ?? '');
  const analyzeMutation = useAnalyzeJob();

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) { setError('Paste a job description first.'); return; }
    if (!selectedResumeId) { setError('Select a resume to match against.'); return; }
    setError('');
    try {
      const result = await analyzeMutation.mutateAsync({
        job_description: jobDescription,
        resume_id: selectedResumeId,
      });
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed. Ensure OPENAI_API_KEY is set.');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Job Intelligence</h1>
        <p className="mt-2 text-muted-foreground">
          Paste a job description and get AI-powered match analysis
        </p>
      </div>

      {/* Input */}
      <div className="bg-card rounded-xl p-6 border space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <label className="text-sm font-medium mb-1 block">Job Description</label>
            <textarea
              placeholder="Paste the full job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={6}
              className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm resize-none"
            />
          </div>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-1 block">Select Resume</label>
              {resumes.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  Upload a resume first on the Resume page.
                </p>
              ) : (
                <select
                  value={selectedResumeId}
                  onChange={(e) => setSelectedResumeId(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
                >
                  <option value="">— choose resume —</option>
                  {resumes.map((r) => (
                    <option key={r.id} value={r.id}>{r.original_filename}</option>
                  ))}
                </select>
              )}
            </div>
            <button
              onClick={handleAnalyze}
              disabled={analyzeMutation.isPending}
              className="w-full py-2.5 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 flex items-center justify-center gap-2 text-sm font-medium transition-colors"
            >
              {analyzeMutation.isPending
                ? <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing...</>
                : <><Search className="w-4 h-4" /> Analyze Job</>}
            </button>
          </div>
        </div>

        {error && (
          <p className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">{error}</p>
        )}
      </div>

      {/* Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Match Score */}
          <div className="bg-card rounded-xl p-6 border">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold">Overall Match</h2>
                <p className="text-muted-foreground text-sm mt-1">
                  Based on your resume vs this job
                </p>
              </div>
              <div className="text-right">
                <p className={`text-5xl font-bold ${
                  analysis.match.overall_match >= 75 ? 'text-green-600' :
                  analysis.match.overall_match >= 50 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {analysis.match.overall_match}%
                </p>
                <p className="text-sm text-muted-foreground">confidence: {analysis.match.confidence_score}%</p>
              </div>
            </div>

            {/* Score breakdown */}
            <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-3">
              {[
                { label: 'Technical', value: analysis.match.technical_match },
                { label: 'Experience', value: analysis.match.experience_match },
                { label: 'Keywords', value: analysis.match.keyword_match },
                { label: 'ATS',       value: analysis.match.ats_match },
                { label: 'Industry',  value: analysis.match.industry_match },
              ].map((item) => (
                <div key={item.label} className="bg-secondary/50 rounded-lg p-3 text-center">
                  <p className="text-xs text-muted-foreground">{item.label}</p>
                  <p className="text-lg font-bold mt-1">{item.value}%</p>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Job Details */}
            <div className="bg-card rounded-xl p-6 border">
              <h3 className="text-lg font-semibold mb-3">Job Overview</h3>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Role</dt>
                  <dd className="font-medium">{analysis.job.job.title}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Company</dt>
                  <dd className="font-medium">{analysis.job.job.company_name}</dd>
                </div>
                {analysis.job.job.location && (
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Location</dt>
                    <dd className="font-medium">{analysis.job.job.location}</dd>
                  </div>
                )}
                {analysis.job.job.seniority && (
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Seniority</dt>
                    <dd className="font-medium capitalize">{analysis.job.job.seniority}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* ATS Analysis */}
            <div className="bg-card rounded-xl p-6 border">
              <h3 className="text-lg font-semibold mb-3">ATS Analysis</h3>
              <div className="space-y-2">
                {[
                  { label: 'Keyword Coverage',  value: analysis.ats_analysis.keyword_coverage },
                  { label: 'Formatting',         value: analysis.ats_analysis.formatting_compatibility },
                  { label: 'Role Alignment',     value: analysis.ats_analysis.role_alignment },
                  { label: 'Section Complete',   value: analysis.ats_analysis.section_completeness },
                ].map((item) => (
                  <div key={item.label}>
                    <div className="flex justify-between text-sm mb-1">
                      <span>{item.label}</span>
                      <span className="font-medium">{item.value}%</span>
                    </div>
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary transition-all"
                        style={{ width: `${item.value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              {analysis.ats_analysis.missing_keywords?.length > 0 && (
                <div className="mt-3">
                  <p className="text-xs font-medium text-muted-foreground mb-1">Missing keywords</p>
                  <div className="flex flex-wrap gap-1">
                    {analysis.ats_analysis.missing_keywords.slice(0, 8).map((kw: string) => (
                      <span key={kw} className="px-2 py-0.5 text-xs bg-destructive/10 text-destructive rounded-full">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Missing Skills */}
          {analysis.missing_skills?.length > 0 && (
            <div className="bg-card rounded-xl p-6 border">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-yellow-500" />
                Skill Gaps
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {analysis.missing_skills.map((skill: any) => (
                  <div key={skill.skill_name} className="p-3 bg-secondary/50 rounded-lg">
                    <p className="font-medium text-sm">{skill.skill_name}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        skill.learning_priority === 'critical'
                          ? 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
                          : skill.learning_priority === 'recommended'
                          ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300'
                          : 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                      }`}>
                        {skill.learning_priority}
                      </span>
                      {skill.difficulty && (
                        <span className="text-xs text-muted-foreground">{skill.difficulty}</span>
                      )}
                    </div>
                    {skill.estimated_learning_time && (
                      <p className="text-xs text-muted-foreground mt-1">{skill.estimated_learning_time}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* AI Insights */}
          {analysis.insights && (
            <div className="bg-card rounded-xl p-6 border">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-primary" />
                AI Insights
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {analysis.insights.top_strengths?.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-green-600 dark:text-green-400 mb-2">
                      ✓ Strengths
                    </p>
                    <ul className="space-y-1">
                      {analysis.insights.top_strengths.map((s: string, i: number) => (
                        <li key={i} className="text-sm flex items-start gap-2">
                          <CheckCircle className="w-3.5 h-3.5 text-green-500 mt-0.5 shrink-0" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {analysis.insights.biggest_weaknesses?.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-red-600 dark:text-red-400 mb-2">
                      ✗ Weaknesses
                    </p>
                    <ul className="space-y-1">
                      {analysis.insights.biggest_weaknesses.map((w: string, i: number) => (
                        <li key={i} className="text-sm flex items-start gap-2">
                          <AlertCircle className="w-3.5 h-3.5 text-red-500 mt-0.5 shrink-0" />
                          {w}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              {analysis.insights.suggested_resume_changes?.length > 0 && (
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm font-medium mb-2">Suggested Resume Changes</p>
                  <ul className="space-y-1">
                    {analysis.insights.suggested_resume_changes.slice(0, 4).map((s: string, i: number) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="text-primary shrink-0">→</span>{s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
