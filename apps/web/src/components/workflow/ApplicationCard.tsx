'use client';

import { Calendar, MapPin, Building2, TrendingUp, AlertCircle } from 'lucide-react';
import { Application } from '@/hooks/api/workflow';

interface ApplicationCardProps {
  application: Application;
  jobTitle?: string;
  companyName?: string;
  location?: string;
  onEdit?: () => void;
  onDelete?: () => void;
}

export function ApplicationCard({ application, jobTitle, companyName, location, onEdit, onDelete }: ApplicationCardProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300';
      case 'low':
        return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getProbabilityColor = (probability: number) => {
    if (probability >= 80) return 'text-green-600 dark:text-green-400';
    if (probability >= 60) return 'text-blue-600 dark:text-blue-400';
    if (probability >= 40) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const daysSinceUpdate = Math.floor((Date.now() - new Date(application.updated_at).getTime()) / (1000 * 60 * 60 * 24));
  const isStale = daysSinceUpdate > 7;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow cursor-pointer">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
            {jobTitle || 'Unknown Position'}
          </h4>
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
            <Building2 className="w-4 h-4" />
            <span>{companyName || 'Unknown Company'}</span>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(application.priority)}`}>
            {application.priority}
          </span>
        </div>
      </div>

      {/* Details */}
      <div className="space-y-2 mb-3">
        {location && (
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
            <MapPin className="w-4 h-4" />
            <span>{location}</span>
          </div>
        )}
        <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
          <Calendar className="w-4 h-4" />
          <span>Updated {daysSinceUpdate} days ago</span>
        </div>
      </div>

      {/* Probability */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-600 dark:text-gray-400">Success Probability</span>
        <div className="flex items-center space-x-2">
          <TrendingUp className={`w-4 h-4 ${getProbabilityColor(application.probability)}`} />
          <span className={`font-semibold ${getProbabilityColor(application.probability)}`}>
            {application.probability}%
          </span>
        </div>
      </div>

      {/* Stale Warning */}
      {isStale && (
        <div className="flex items-center space-x-2 text-xs text-orange-600 dark:text-orange-400 mb-3">
          <AlertCircle className="w-4 h-4" />
          <span>No updates for {daysSinceUpdate} days</span>
        </div>
      )}

      {/* Notes Preview */}
      {application.notes && (
        <div className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
          {application.notes}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center space-x-2 pt-3 border-t border-gray-200 dark:border-gray-700">
        <button
          onClick={onEdit}
          className="flex-1 px-3 py-2 text-sm bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors"
        >
          View Details
        </button>
        {onDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
            className="px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
}
