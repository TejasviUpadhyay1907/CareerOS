'use client';

import { Calendar, Clock, CheckCircle, AlertCircle, FileText, MessageSquare, User } from 'lucide-react';
import { TimelineEvent } from '@/hooks/api/workflow';

interface TimelineViewProps {
  events: TimelineEvent[];
}

export function TimelineView({ events }: TimelineViewProps) {
  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'resume_generated':
        return <FileText className="w-4 h-4" />;
      case 'applied':
        return <CheckCircle className="w-4 h-4" />;
      case 'recruiter_replied':
        return <MessageSquare className="w-4 h-4" />;
      case 'oa_scheduled':
      case 'interview_scheduled':
        return <Calendar className="w-4 h-4" />;
      case 'interview_completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'offer_received':
        return <CheckCircle className="w-4 h-4" />;
      case 'rejected':
        return <AlertCircle className="w-4 h-4" />;
      case 'followup_sent':
        return <MessageSquare className="w-4 h-4" />;
      case 'note_added':
        return <FileText className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case 'offer_received':
        return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      case 'rejected':
        return 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400';
      case 'interview_scheduled':
      case 'oa_scheduled':
        return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400';
      case 'applied':
        return 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400';
      default:
        return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  if (events.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
        <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No timeline events yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <div key={event.id} className="flex items-start space-x-4">
          {/* Timeline Line */}
          {index !== events.length - 1 && (
            <div className="absolute left-6 mt-8 w-0.5 h-full bg-gray-200 dark:bg-gray-700" />
          )}

          {/* Icon */}
          <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${getEventColor(event.event_type)}`}>
            {getEventIcon(event.event_type)}
          </div>

          {/* Content */}
          <div className="flex-1 pb-4">
            <div className="flex items-center justify-between mb-1">
              <h4 className="font-medium text-gray-900 dark:text-gray-100">{event.title}</h4>
              <span className="text-sm text-gray-500 dark:text-gray-400">{formatDate(event.event_date)}</span>
            </div>
            {event.description && (
              <p className="text-sm text-gray-600 dark:text-gray-400">{event.description}</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
