'use client';

import { useState } from 'react';
import { ResumeUploader } from '@/components/resume/ResumeUploader';
import { HealthScoreCard } from '@/components/resume/HealthScoreCard';
import { SummaryCard } from '@/components/resume/SummaryCard';
import { SkillsGrid } from '@/components/resume/SkillsGrid';
import { Timeline } from '@/components/resume/Timeline';
import { RecommendationCard } from '@/components/resume/RecommendationCard';
import { useAuth } from '@/components/providers/auth-provider';
import { useUploadResume, useAnalyzeResume } from '@/hooks/api/resume';
import { Loader2 } from 'lucide-react';

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

    // Upload
    const uploadResult = await uploadMutation.mutateAsync({ file, userId: user.id });
    setResumeId(uploadResult.id);

    // Analyze with AI — show spinner
    setAnalyzing(true);
    try {
      const analysis = await analyzeMutation.mutateAsync(uploadResult.id);
      setResumeData({
        healthScore: analysis.analysis.health_score,
        healthBreakdown: analysis.analysis.health_breakdown,
        summary: {
          totalExperience: analysis.metadata.years_of_experience ?? 0,
          skills: [],
          education: analysis.metadata.primary_domain ?? '',
          projects: analysis.metadata.total_projects,
          certifications: analysis.metadata.total_certifications,
        },
        skills: [],
        timelineItems: [],
        recommendations: analysis.analysis.recommendations.map((r: string) => ({
          title: 'Recommendation',
          description: r,
        })),
        strengths: analysis.analysis.strengths,
        weaknesses: analysis.analysis.weaknesses,
      });
    } catch (err) {
      setAnalysisError(
        err instanceof Error ? err.message : 'AI analysis unavailable.'
      );
      setResumeData({
        healthScore: 0,
        healthBreakdown: {},
        summary: { totalExperience: 0, skills: [], education: '', projects: 0, certifications: 0 },
        skills: [],
        timelineItems: [],
        recommendations: [],
        strengths: [],
        weaknesses: [],
      });
    } finally {
      setAnalyzing(false);
    }
  };

  // Show AI analysis spinner after upload
  if (analyzing) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Resume Intelligence</h1>
          <p className="mt-2 text-muted-foreground">Upload your resume and get AI-powered insights</p>
        </div>
        <div className="flex flex-col items-center justify-center py-24 bg-card rounded-xl border">
          <Loader2 className="w-12 h-12 animate-spin text-primary mb-4" />
          <p className="text-lg font-medium">AI is analyzing your resume...</p>
          <p className="text-sm text-muted-foreground mt-2">This takes 10–20 seconds. Please wait.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Resume Intelligence</h1>
        <p className="mt-2 text-muted-foreground">
          Upload your resume and get AI-powered insights
        </p>
      </div>

      {!resumeData ? (
        <ResumeUploader onUpload={handleUpload} userId={user?.id ?? ''} />
      ) : (
        <div className="space-y-6">
          {analysisError && (
            <div className="bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg px-4 py-3 text-sm text-yellow-800 dark:text-yellow-200">
              ⚠️ {analysisError}
            </div>
          )}

          {resumeId && (
            <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg px-4 py-3 text-sm text-green-800 dark:text-green-200">
              ✓ Resume uploaded and stored (ID: {resumeId})
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <HealthScoreCard
              score={resumeData.healthScore}
              breakdown={resumeData.healthBreakdown}
            />
            <SummaryCard summary={resumeData.summary} />
          </div>

          {resumeData.skills.length > 0 && (
            <SkillsGrid skills={resumeData.skills} />
          )}

          {resumeData.timelineItems.length > 0 && (
            <Timeline items={resumeData.timelineItems} type="experience" />
          )}

          {resumeData.recommendations.length > 0 && (
            <div>
              <h2 className="text-2xl font-semibold mb-4">AI Recommendations</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {resumeData.recommendations.map((rec: any, index: number) => (
                  <RecommendationCard key={index} {...rec} />
                ))}
              </div>
            </div>
          )}

          <button
            onClick={() => { setResumeData(null); setResumeId(null); setAnalysisError(null); }}
            className="px-4 py-2 bg-secondary hover:bg-secondary/80 rounded-lg transition-colors text-sm"
          >
            Upload different resume
          </button>
        </div>
      )}
    </div>
  );
}
