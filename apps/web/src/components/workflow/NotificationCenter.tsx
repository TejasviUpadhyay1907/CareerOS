'use client';

import { Bell, X, Check, AlertCircle, Info, CheckCircle2, Clock } from 'lucide-react';
import { Notification } from '@/hooks/api/workflow';

interface NotificationCenterProps {
  notifications: Notification[];
  onMarkRead?: (notificationId: string) => void;
  onDismiss?: (notificationId: string) => void;
}

export function NotificationCenter({ notifications, onMarkRead, onDismiss }: NotificationCenterProps) {
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'reminder':
        return <Clock className="w-4 h-4" />;
      case 'recommendation':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'alert':
        return <AlertCircle className="w-4 h-4" />;
      case 'update':
        return <Info className="w-4 h-4" />;
      default:
        return <Bell className="w-4 h-4" />;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'alert':
        return 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400';
      case 'reminder':
        return 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400';
      case 'recommendation':
        return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      case 'update':
        return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400';
      default:
        return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'border-l-4 border-red-500';
      case 'medium':
        return 'border-l-4 border-yellow-500';
      case 'low':
        return 'border-l-4 border-green-500';
      default:
        return 'border-l-4 border-gray-500';
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bell className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Notifications</h3>
          {unreadCount > 0 && (
            <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400 rounded-full">
              {unreadCount} new
            </span>
          )}
        </div>
        <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
          Mark all as read
        </button>
      </div>

      {/* Notifications List */}
      {notifications.length === 0 ? (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          <Bell className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No notifications</p>
        </div>
      ) : (
        <div className="space-y-2">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 ${
                !notification.is_read ? 'bg-blue-50 dark:bg-blue-900/10' : ''
              } ${getPriorityColor(notification.priority)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${getNotificationColor(notification.notification_type)}`}>
                    {getNotificationIcon(notification.notification_type)}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-1">
                      {notification.title}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {notification.message}
                    </p>
                    <span className="text-xs text-gray-500 dark:text-gray-500">
                      {new Date(notification.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {!notification.is_read && (
                    <button
                      onClick={() => onMarkRead?.(notification.id)}
                      className="p-1 text-gray-400 hover:text-green-600 dark:hover:text-green-400 transition-colors"
                      title="Mark as read"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    onClick={() => onDismiss?.(notification.id)}
                    className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                    title="Dismiss"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
              {notification.action_url && (
                <button className="mt-3 text-sm text-blue-600 dark:text-blue-400 hover:underline">
                  View details
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
