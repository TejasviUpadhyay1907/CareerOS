'use client';

import { Building2, Globe, MapPin, Users, FileText, MessageSquare, Calendar } from 'lucide-react';
import { CompanyProfile, Application } from '@/hooks/api/workflow';

interface CompanyWorkspaceProps {
  company: CompanyProfile;
  applications: Application[];
  onAddApplication?: () => void;
  onEditCompany?: () => void;
}

export function CompanyWorkspace({ company, applications, onAddApplication, onEditCompany }: CompanyWorkspaceProps) {
  return (
    <div className="space-y-6">
      {/* Company Header */}
      <div className="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl p-6 text-white">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">{company.name}</h2>
            <div className="flex items-center space-x-4 text-purple-100">
              {company.industry && (
                <div className="flex items-center space-x-1">
                  <Building2 className="w-4 h-4" />
                  <span>{company.industry}</span>
                </div>
              )}
              {company.size && (
                <div className="flex items-center space-x-1">
                  <Users className="w-4 h-4" />
                  <span>{company.size}</span>
                </div>
              )}
              {company.location && (
                <div className="flex items-center space-x-1">
                  <MapPin className="w-4 h-4" />
                  <span>{company.location}</span>
                </div>
              )}
            </div>
          </div>
          <button
            onClick={onEditCompany}
            className="px-4 py-2 bg-white/20 backdrop-blur rounded-lg hover:bg-white/30 transition-colors"
          >
            Edit Profile
          </button>
        </div>
      </div>

      {/* Company Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {company.website && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-2">
              <Globe className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              <h3 className="font-medium text-gray-900 dark:text-gray-100">Website</h3>
            </div>
            <a
              href={company.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              {company.website}
            </a>
          </div>
        )}
        {company.description && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-2 mb-2">
              <FileText className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              <h3 className="font-medium text-gray-900 dark:text-gray-100">Description</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">{company.description}</p>
          </div>
        )}
      </div>

      {/* Applications */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Applications</h3>
          <button
            onClick={onAddApplication}
            className="px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors"
          >
            Add Application
          </button>
        </div>

        {applications.length === 0 ? (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <Building2 className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No applications yet</p>
          </div>
        ) : (
          <div className="space-y-3">
            {applications.map((application) => (
              <div
                key={application.id}
                className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-gray-100">
                      {application.metadata?.job_title || 'Unknown Position'}
                    </h4>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      Status: <span className="capitalize">{application.status.replace('_', ' ')}</span>
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full">
                      {application.priority}
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center space-x-1">
                    <Calendar className="w-4 h-4" />
                    <span>Applied {new Date(application.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <MessageSquare className="w-4 h-4" />
                    <span>Probability: {application.probability}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Notes */}
      {company.notes && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <FileText className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            <h3 className="font-medium text-gray-900 dark:text-gray-100">Notes</h3>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{company.notes}</p>
        </div>
      )}
    </div>
  );
}
