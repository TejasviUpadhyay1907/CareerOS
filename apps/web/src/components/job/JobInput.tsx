'use client';

import { useState } from 'react';
import { Briefcase, Loader2, Sparkles } from 'lucide-react';

interface JobInputProps {
  onAnalyze: (jobDescription: string, resumeId: string) => void;
  isLoading?: boolean;
  resumeId?: string;
}

export function JobInput({ onAnalyze, isLoading = false, resumeId }: JobInputProps) {
  const [jobDescription, setJobDescription] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    if (jobDescription.length < 50) {
      setError('Job description is too short. Please provide more details.');
      return;
    }

    if (!resumeId) {
      setError('Please select a resume first');
      return;
    }

    onAnalyze(jobDescription, resumeId);
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-4">
        <Briefcase className="w-6 h-6 text-blue-600 dark:text-blue-400" />
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
          Analyze Job Description
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="job-description"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Paste Job Description
          </label>
          <textarea
            id="job-description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the complete job description here including requirements, responsibilities, qualifications, and benefits..."
            className="w-full h-48 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-gray-100 resize-none"
            disabled={isLoading}
          />
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {jobDescription.length} characters
          </p>
        </div>

        {error && (
          <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Analyze Job</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <p className="text-sm text-blue-700 dark:text-blue-300">
          <strong>Tip:</strong> Include the complete job description for the best analysis results.
          The AI will extract skills, requirements, and match them against your resume.
        </p>
      </div>
    </div>
  );
}
