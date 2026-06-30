'use client';

import { Building2, GraduationCap, Calendar } from 'lucide-react';

interface TimelineItem {
  title: string;
  subtitle: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  is_current?: boolean;
  description?: string;
  achievements?: string[];
}

interface TimelineProps {
  items: TimelineItem[];
  type: 'experience' | 'education';
}

export function Timeline({ items, type }: TimelineProps) {
  const formatDate = (date?: string) => {
    if (!date) return 'Present';
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    });
  };

  const getIcon = () => {
    return type === 'experience' ? (
      <Building2 className="w-5 h-5" />
    ) : (
      <GraduationCap className="w-5 h-5" />
    );
  };

  const getIconColor = () => {
    return type === 'experience'
      ? 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400'
      : 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400';
  };

  if (items.length === 0) {
    return (
      <div className="border rounded-xl p-6 text-center text-gray-500 dark:text-gray-400">
        No {type} detected
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 capitalize">
        {type}
      </h3>

      <div className="space-y-6">
        {items.map((item, index) => (
          <div key={index} className="relative pl-8 pb-6 last:pb-0">
            {index !== items.length - 1 && (
              <div className="absolute left-[19px] top-8 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />
            )}

            <div className={`absolute left-0 top-0 p-2 rounded-full ${getIconColor()}`}>
              {getIcon()}
            </div>

            <div className="space-y-2">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">
                    {item.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {item.subtitle}
                  </p>
                </div>
                {item.is_current && (
                  <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 rounded-full">
                    Current
                  </span>
                )}
              </div>

              {item.location && (
                <p className="text-sm text-gray-500 dark:text-gray-400">{item.location}</p>
              )}

              <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                <Calendar className="w-4 h-4" />
                <span>
                  {formatDate(item.start_date)} - {formatDate(item.end_date)}
                </span>
              </div>

              {item.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  {item.description}
                </p>
              )}

              {item.achievements && item.achievements.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {item.achievements.map((achievement, achIndex) => (
                    <li
                      key={achIndex}
                      className="text-sm text-gray-600 dark:text-gray-400 flex items-start"
                    >
                      <span className="mr-2">•</span>
                      <span>{achievement}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
