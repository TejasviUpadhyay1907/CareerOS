'use client';

import { Download, FileText, Copy } from 'lucide-react';

interface DocumentExportPanelProps {
  content: string;
  title: string;
  onExport?: (format: string) => void;
}

export function DocumentExportPanel({ content, title, onExport }: DocumentExportPanelProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  const handleDownload = (format: string) => {
    if (onExport) {
      onExport(format);
    } else {
      // Fallback: create a blob and download
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title.replace(/\s+/g, '_')}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="border rounded-xl p-6 bg-white dark:bg-gray-800">
      <div className="flex items-center space-x-3 mb-6">
        <FileText className="w-6 h-6 text-gray-600 dark:text-gray-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Export Document
        </h3>
      </div>

      <div className="space-y-4">
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Document Title</p>
          <p className="font-medium text-gray-900 dark:text-gray-100">{title}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => handleCopy()}
            className="flex items-center justify-center space-x-2 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors"
          >
            <Copy className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <span className="font-medium text-blue-600 dark:text-blue-400">Copy to Clipboard</span>
          </button>

          <button
            onClick={() => handleDownload('txt')}
            className="flex items-center justify-center space-x-2 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800 hover:bg-green-100 dark:hover:bg-green-900/40 transition-colors"
          >
            <Download className="w-5 h-5 text-green-600 dark:text-green-400" />
            <span className="font-medium text-green-600 dark:text-green-400">Download as TXT</span>
          </button>

          <button
            onClick={() => handleDownload('md')}
            className="flex items-center justify-center space-x-2 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800 hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-colors"
          >
            <Download className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <span className="font-medium text-purple-600 dark:text-purple-400">Download as Markdown</span>
          </button>

          <button
            onClick={() => handleDownload('pdf')}
            className="flex items-center justify-center space-x-2 p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800 hover:bg-orange-100 dark:hover:bg-orange-900/40 transition-colors"
          >
            <Download className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            <span className="font-medium text-orange-600 dark:text-orange-400">Download as PDF</span>
          </button>
        </div>
      </div>
    </div>
  );
}
