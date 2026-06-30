'use client';

import { useState } from 'react';
import { FileText, RefreshCw, Download, Copy } from 'lucide-react';
import { CoverLetter } from '@/hooks/api/accelerator';

interface CoverLetterEditorProps {
  coverLetter: CoverLetter;
  onRegenerate?: () => void;
  onEdit?: (content: string) => void;
}

export function CoverLetterEditor({ coverLetter, onRegenerate, onEdit }: CoverLetterEditorProps) {
  const [content, setContent] = useState(coverLetter.content);
  const [isEditing, setIsEditing] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  const handleEdit = () => {
    if (isEditing && onEdit) {
      onEdit(content);
    }
    setIsEditing(!isEditing);
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Cover Letter
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {coverLetter.company_name} - {coverLetter.role_title}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Copy to clipboard"
          >
            <Copy className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
          <button
            onClick={handleEdit}
            className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {isEditing ? 'Save' : 'Edit'}
          </button>
          {onRegenerate && (
            <button
              onClick={onRegenerate}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="Regenerate"
            >
              <RefreshCw className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </button>
          )}
        </div>
      </div>

      {/* Metadata */}
      <div className="flex items-center space-x-4 mb-4">
        <span className="px-2 py-1 text-xs bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300 rounded-full">
          {coverLetter.tone}
        </span>
        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full">
          {coverLetter.length}
        </span>
      </div>

      {/* Personalization Points */}
      {coverLetter.personalization_points && coverLetter.personalization_points.length > 0 && (
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Personalization Points</p>
          <div className="flex flex-wrap gap-2">
            {coverLetter.personalization_points.map((point, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 rounded-full"
              >
                {point.point}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Content Editor */}
      <div className="relative">
        {isEditing ? (
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full h-96 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 resize-none"
          />
        ) : (
          <div className="w-full h-96 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900 overflow-y-auto">
            <div className="whitespace-pre-wrap text-gray-900 dark:text-gray-100">{content}</div>
          </div>
        )}
      </div>
    </div>
  );
}
