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

export default function ResumePage() {
  const { user } = useAuth();
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [resumeData, setResumeData] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const uploadMutation = useUploadResume();
  const analyzeMutation = useAnalyzeResume();

  const handleUpload = async (file: File) => {
    if (!user?.id) throw new Error('Not authenticated');
    setAnalysisError(null);

    // Upload
    const uploadResult = await uploadMutation.mutateAsync({ file, userId: user.id });
    setResumeId(uploadResult.id);

    // Analyze with AI
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
      // AI may not be configured — still show the upload succeeded
      setAnalysisError(
        err instanceof Error ? err.message : 'AI analysis unavailable. Configure OPENAI_API_KEY to enable.'
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
    }
  };

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
