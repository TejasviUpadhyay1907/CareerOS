'use client';

import { useState } from 'react';
import { useAuth } from '@/components/providers/auth-provider';
import { useUploadResume, useAnalyzeResume } from '@/hooks/api/resume';
import { ResumeUploader } from '@/components/resume/ResumeUploader';
import { HealthScoreCard } from '@/components/resume/HealthScoreCard';
import { Loader2, CheckCircle, AlertTriangle, RefreshCw, Lightbulb } from 'lucide-react';

export default function ResumePage() {
  const { user } = useAuth();
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [resumeData, setResumeData] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  const uploadMutation = useUploadResume();
  const analyzeMutation = useAnalyzeResume();

  const handleUpload = async (file: File) => {
    if (!user?.id) throw new Error('Not authenticated');
    setAnalysisError(null);
    setResumeData(null);

    const uploadResult = await uploadMutation.mutateAsync({ file, userId: user.id });
    setResumeId(uploadResult.id);

    setAnalyzing(true);
    try {
      const analysis = await analyzeMutation.mutateAsync(uploadResult.id);
      setResumeData(analysis);
    } catch (err) {
      setAnalysisError(err instanceof Error ? err.message : 'AI analysis failed.');
    } finally {
      setAnalyzing(false);
    }
  };

  // ── Loading ────────────────────────────────────────────────────────────
  if (analyzing) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Resume Intelligence</h1>
          <p className="mt-2 text-muted-foreground">Upload your resume and get AI-powered insights</p>
        </div>
        <div className="flex flex-col items-center justify-center py-24 bg-card rounded-xl border">
          <Loader2 className="w-14 h-14 animate-spin text-primary mb-5" />
          <p className="text-xl font-semibold">AI is analyzing your resume...</p>
          <p className="text-sm text-muted-foreground mt-2 max-w-xs text-center">
            Extracting skills, calculating health score, generating insights. This takes 10–20 seconds.
          </p>
        </div>
      </div>
    );
  }

  // ── Results ────────────────────────────────────────────────────────────
  if (resumeData) {
    const analysis       = resumeData.analysis ?? {};
    const metadata       = resumeData.metadata ?? {};
    const healthScore    = analysis.health_score ?? 0;
    const healthBreakdown= analysis.health_breakdown ?? {};
    const strengths      = Array.isArray(analysis.strengths) ? analysis.strengths : [];
    const weaknesses     = Array.isArray(analysis.weaknesses) ? analysis.weaknesses : [];
    const recommendations= Array.isArray(analysis.recommendations) ? analysis.recommendations : [];
    const domain         = metadata.primary_domain ?? 'N/A';
    const yearsExp       = metadata.years_of_experience ?? 0;
    const totalProjects  = metadata.total_projects ?? 0;
    const totalCerts     = metadata.total_certifications ?? 0;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Resume Intelligence</h1>
            <p className="mt-1 text-muted-foreground">AI-powered analysis of your resume</p>
          </div>
          <button
            onClick={() => { setResumeData(null); setResumeId(null); setAnalysisError(null); }}
            className="flex items-center gap-2 px-4 py-2 border rounded-lg text-sm hover:bg-secondary transition-colors"
          >
            <RefreshCw className="w-4 h-4" /> Upload New
          </button>
        </div>

        <div className="flex items-center gap-2 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg px-4 py-3 text-sm text-green-800 dark:text-green-200">
          <CheckCircle className="w-4 h-4 shrink-0" />
          Resume uploaded and analyzed successfully!
        </div>

        {analysisError && (
          <div className="flex items-start gap-2 bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg px-4 py-3 text-sm text-yellow-800 dark:text-yellow-200">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            {analysisError}
          </div>
        )}

        {/* Score + Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-1">
            <HealthScoreCard score={healthScore} breakdown={healthBreakdown} />
          </div>
          <div className="md:col-span-2 grid grid-cols-2 gap-4">
            <div className="bg-card border rounded-xl p-5">
              <p className="text-xs text-muted-foreground mb-1">Domain</p>
              <p className="text-lg font-bold text-primary">{domain}</p>
            </div>
            <div className="bg-card border rounded-xl p-5">
              <p className="text-xs text-muted-foreground mb-1">Experience</p>
              <p className="text-lg font-bold">{yearsExp > 0 ? `${yearsExp} yr${yearsExp !== 1 ? 's' : ''}` : 'Fresher'}</p>
            </div>
            <div className="bg-card border rounded-xl p-5">
              <p className="text-xs text-muted-foreground mb-1">Projects</p>
              <p className="text-lg font-bold">{totalProjects}</p>
            </div>
            <div className="bg-card border rounded-xl p-5">
              <p className="text-xs text-muted-foreground mb-1">Certifications</p>
              <p className="text-lg font-bold">{totalCerts}</p>
            </div>
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        {(strengths.length > 0 || weaknesses.length > 0) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {strengths.length > 0 && (
              <div className="bg-card border rounded-xl p-5">
                <h3 className="font-semibold mb-3 text-green-600 dark:text-green-400">✓ Strengths</h3>
                <ul className="space-y-2">
                  {strengths.map((s: string, i: number) => (
                    <li key={i} className="text-sm flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {weaknesses.length > 0 && (
              <div className="bg-card border rounded-xl p-5">
                <h3 className="font-semibold mb-3 text-orange-600 dark:text-orange-400">⚠ Areas to Improve</h3>
                <ul className="space-y-2">
                  {weaknesses.map((w: string, i: number) => (
                    <li key={i} className="text-sm flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 text-orange-500 mt-0.5 shrink-0" />
                      {w}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* AI Recommendations */}
        {recommendations.length > 0 && (
          <div className="bg-card border rounded-xl p-5">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-yellow-500" /> AI Recommendations
            </h3>
            <ul className="space-y-2">
              {recommendations.map((rec: string, i: number) => (
                <li key={i} className="text-sm flex items-start gap-2">
                  <span className="text-yellow-500 shrink-0 mt-0.5">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // ── Upload form ────────────────────────────────────────────────────────
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Resume Intelligence</h1>
        <p className="mt-2 text-muted-foreground">Upload your resume and get AI-powered insights</p>
      </div>
      <ResumeUploader onUpload={handleUpload} userId={user?.id ?? ''} />
    </div>
  );
}
