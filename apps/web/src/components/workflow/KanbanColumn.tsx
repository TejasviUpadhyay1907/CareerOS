'use client';

import { Application } from '@/hooks/api/workflow';
import { ApplicationCard } from './ApplicationCard';

interface KanbanColumnProps {
  id: string;
  title: string;
  status: string;
  applications: Application[];
  onApplicationClick?: (application: Application) => void;
  onApplicationEdit?: (application: Application) => void;
  onApplicationDelete?: (application: Application) => void;
}

export function KanbanColumn({
  id,
  title,
  status,
  applications,
  onApplicationClick,
  onApplicationEdit,
  onApplicationDelete,
}: KanbanColumnProps) {
  return (
    <div className="flex-shrink-0 w-80 bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
      {/* Column Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
        <span className="px-2 py-1 text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full">
          {applications.length}
        </span>
      </div>

      {/* Applications List */}
      <div className="space-y-3">
        {applications.length === 0 ? (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400 text-sm">
            No applications
          </div>
        ) : (
          applications.map((application) => (
            <ApplicationCard
              key={application.id}
              application={application}
              jobTitle={application.metadata?.job_title}
              companyName={application.metadata?.company_name}
              location={application.metadata?.location}
              onEdit={() => onApplicationEdit?.(application)}
              onDelete={() => onApplicationDelete?.(application)}
            />
          ))
        )}
      </div>
    </div>
  );
}
