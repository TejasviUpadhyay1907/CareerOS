'use client';

import { Clock, FileText, MessageSquare, CheckCircle2, AlertCircle, Building2, User, Calendar } from 'lucide-react';

interface ActivityFeedProps {
  activities: Array<{
    action: string;
    entity_type: string;
    entity_id?: string;
    created_at: string;
    metadata?: Record<string, any>;
  }>;
}

export function ActivityFeed({ activities }: ActivityFeedProps) {
  const getActivityIcon = (action: string) => {
    switch (action) {
      case 'create_application':
        return <Building2 className="w-4 h-4" />;
      case 'update_application':
        return <FileText className="w-4 h-4" />;
      case 'create_task':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'complete_task':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'send_message':
        return <MessageSquare className="w-4 h-4" />;
      case 'add_note':
        return <FileText className="w-4 h-4" />;
      case 'schedule_interview':
        return <Calendar className="w-4 h-4" />;
      case 'receive_offer':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'rejected':
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const getActivityColor = (action: string) => {
    switch (action) {
      case 'receive_offer':
        return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      case 'rejected':
        return 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400';
      case 'schedule_interview':
        return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400';
      case 'create_application':
        return 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400';
      default:
        return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const formatAction = (action: string) => {
    return action.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
  };

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
        <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No recent activity</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {activities.map((activity, index) => (
        <div
          key={index}
          className="flex items-start space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
        >
          <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${getActivityColor(activity.action)}`}>
            {getActivityIcon(activity.action)}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h4 className="font-medium text-gray-900 dark:text-gray-100 text-sm">
                {formatAction(activity.action)}
              </h4>
              <span className="text-xs text-gray-500 dark:text-gray-400">{formatTime(activity.created_at)}</span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400 capitalize">
              {activity.entity_type.replace(/_/g, ' ')}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
