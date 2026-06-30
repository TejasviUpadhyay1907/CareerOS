'use client';

import { useState } from 'react';
import { Briefcase, FileText, MessageSquare, Calendar, Clock, Building2, TrendingUp, CheckCircle2, Brain } from 'lucide-react';
import { Application, TimelineEvent, Task } from '@/hooks/api/workflow';
import { TimelineView } from './TimelineView';
import { TaskPanel } from './TaskPanel';
import { ApplicationInsights } from './ApplicationInsights';

interface CareerCaseViewProps {
  application: Application;
  resume: any;
  job: any;
  company?: any;
  timeline: TimelineEvent[];
  tasks: Task[];
  notes: any[];
  documents: any[];
  aiInsights: any;
}

export function CareerCaseView({
  application,
  resume,
  job,
  company,
  timeline,
  tasks,
  notes,
  documents,
  aiInsights,
}: CareerCaseViewProps) {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Briefcase className="w-5 h-5" />
              <span className="text-sm font-medium text-indigo-100">Career Case</span>
            </div>
            <h2 className="text-2xl font-bold mb-1">{job?.title || 'Unknown Position'}</h2>
            <div className="flex items-center space-x-4 text-indigo-100">
              <div className="flex items-center space-x-1">
                <Building2 className="w-4 h-4" />
                <span>{company?.name || job?.company_name || 'Unknown Company'}</span>
              </div>
              <div className="flex items-center space-x-1">
                <TrendingUp className="w-4 h-4" />
                <span>{application.probability}% success probability</span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              application.status === 'offer' ? 'bg-green-400 text-green-900' :
              application.status === 'interview' ? 'bg-blue-400 text-blue-900' :
              application.status === 'rejected' ? 'bg-red-400 text-red-900' :
              'bg-white/20'
            }`}>
              {application.status.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'overview'
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Overview</span>
          </button>
          <button
            onClick={() => setActiveTab('timeline')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'timeline'
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
          >
            <Clock className="w-4 h-4" />
            <span>Timeline</span>
          </button>
          <button
            onClick={() => setActiveTab('tasks')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'tasks'
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Tasks</span>
          </button>
          <button
            onClick={() => setActiveTab('insights')}
            className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === 'insights'
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
          >
            <Brain className="w-4 h-4" />
            <span>AI Insights</span>
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Application Details */}
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Application Details</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Status</p>
                    <p className="font-medium text-gray-900 dark:text-gray-100 capitalize">{application.status.replace('_', ' ')}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Priority</p>
                    <p className="font-medium text-gray-900 dark:text-gray-100 capitalize">{application.priority}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Applied Date</p>
                    <p className="font-medium text-gray-900 dark:text-gray-100">{new Date(application.created_at).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Last Updated</p>
                    <p className="font-medium text-gray-900 dark:text-gray-100">{new Date(application.updated_at).toLocaleDateString()}</p>
                  </div>
                </div>
                {application.notes && (
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Notes</p>
                    <p className="text-gray-900 dark:text-gray-100">{application.notes}</p>
                  </div>
                )}
              </div>

              {/* Documents */}
              {documents.length > 0 && (
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Documents</h3>
                  <div className="space-y-2">
                    {documents.map((doc, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <FileText className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                          <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{doc.type}</span>
                        </div>
                        <span className="text-xs text-gray-500 dark:text-gray-400">v{doc.version}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'timeline' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <TimelineView events={timeline} />
            </div>
          )}

          {activeTab === 'tasks' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <TaskPanel
                tasks={tasks}
                onCreateTask={() => {}}
                onToggleTask={() => {}}
                onDeleteTask={() => {}}
              />
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <ApplicationInsights application={application} aiInsights={aiInsights} />
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* AI Insights Summary */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Quick Insights</h3>
            <div className="space-y-3">
              {aiInsights.next_best_action && (
                <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <p className="text-xs text-purple-600 dark:text-purple-400 mb-1">Next Action</p>
                  <p className="text-sm text-gray-900 dark:text-gray-100">{aiInsights.next_best_action}</p>
                </div>
              )}
              {aiInsights.urgency && (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Urgency</span>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    aiInsights.urgency === 'high' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400' :
                    aiInsights.urgency === 'medium' ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400' :
                    'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400'
                  }`}>
                    {aiInsights.urgency}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full px-4 py-2 text-sm bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors text-left">
                Update Status
              </button>
              <button className="w-full px-4 py-2 text-sm bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/40 transition-colors text-left">
                Add Note
              </button>
              <button className="w-full px-4 py-2 text-sm bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-colors text-left">
                Schedule Follow-up
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
