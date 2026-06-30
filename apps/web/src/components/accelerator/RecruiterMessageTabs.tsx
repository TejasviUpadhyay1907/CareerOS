'use client';

import { useState } from 'react';
import { MessageSquare, Copy, RefreshCw } from 'lucide-react';
import { RecruiterMessage } from '@/hooks/api/accelerator';

interface RecruiterMessageTabsProps {
  messages: RecruiterMessage[];
  onRegenerate?: (messageType: string) => void;
}

export function RecruiterMessageTabs({ messages, onRegenerate }: RecruiterMessageTabsProps) {
  const [activeTab, setActiveTab] = useState(0);

  if (messages.length === 0) {
    return (
      <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
        <div className="flex items-center space-x-3 mb-4">
          <MessageSquare className="w-6 h-6 text-purple-600 dark:text-purple-400" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Recruiter Outreach
          </h3>
        </div>
        <p className="text-gray-600 dark:text-gray-400 text-center">No messages generated yet</p>
      </div>
    );
  }

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="border rounded-xl bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 p-6 border-b border-gray-200 dark:border-gray-700">
        <MessageSquare className="w-6 h-6 text-purple-600 dark:text-purple-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Recruiter Outreach
        </h3>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 overflow-x-auto">
        {messages.map((message, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
              activeTab === index
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
          >
            {message.message_type.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-6">
        {messages.map((message, index) => (
          <div key={index} className={activeTab === index ? 'block' : 'hidden'}>
            {/* Metadata */}
            <div className="flex items-center space-x-4 mb-4">
              <span className="px-2 py-1 text-xs bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300 rounded-full">
                {message.tone}
              </span>
              <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full">
                {message.length}
              </span>
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 rounded-full">
                {message.platform}
              </span>
            </div>

            {/* Subject (if applicable) */}
            {message.subject && (
              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Subject</p>
                <p className="text-gray-900 dark:text-gray-100">{message.subject}</p>
              </div>
            )}

            {/* Content */}
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Message</p>
              <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">{message.content}</p>
              </div>
            </div>

            {/* Personalization Reason */}
            {message.personalization_reason && (
              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Personalization Reason</p>
                <p className="text-gray-600 dark:text-gray-400 text-sm">{message.personalization_reason}</p>
              </div>
            )}

            {/* Call to Action */}
            {message.call_to_action && (
              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Call to Action</p>
                <p className="text-blue-600 dark:text-blue-400 text-sm">{message.call_to_action}</p>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleCopy(message.content)}
                className="flex items-center space-x-2 px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </button>
              {onRegenerate && (
                <button
                  onClick={() => onRegenerate(message.message_type)}
                  className="flex items-center space-x-2 px-3 py-2 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>Regenerate</span>
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
