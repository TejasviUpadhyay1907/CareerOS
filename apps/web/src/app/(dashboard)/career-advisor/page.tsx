'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, TrendingUp, Target, Loader2 } from 'lucide-react';
import { useAuth } from '@/components/providers/auth-provider';
import { useResumes } from '@/hooks/api/resume';
import { useApplications } from '@/hooks/api/workflow';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function CareerAdvisorPage() {
  const { user } = useAuth();
  const { data: resumes = [] } = useResumes(user?.id ?? '');
  const { data: applications = [] } = useApplications();

  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hello! I'm your AI Career Advisor. I can help you with career planning, resume improvement, interview prep, and job search strategies. What would you like to discuss today?",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const buildContext = () => {
    const parts: string[] = [];
    if (user) parts.push(`User: ${user.first_name ?? ''} ${user.last_name ?? ''} (${user.email})`);
    if (resumes.length > 0) parts.push(`Uploaded resumes: ${resumes.map((r) => r.original_filename).join(', ')}`);
    if (applications.length > 0) {
      const summary = applications.slice(0, 5).map((a) => `${a.status}`).join(', ');
      parts.push(`Applications: ${applications.length} total (recent statuses: ${summary})`);
    }
    return parts.join('\n');
  };

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput('');

    const userMsg: Message = { role: 'user', content: text };
    const updated = [...messages, userMsg];
    setMessages(updated);
    setLoading(true);

    try {
      const token = localStorage.getItem('careeros_token');
      const res = await fetch(`${API_BASE}/api/v1/career/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          messages: updated.map((m) => ({ role: m.role, content: m.content })),
          context: buildContext(),
        }),
      });

      if (res.ok) {
        const data = await res.json() as { reply: string };
        setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
      } else {
        const errorData = await res.json().catch(() => ({ reply: 'API error occurred' }));
        setMessages((prev) => [...prev, { role: 'assistant', content: errorData.reply || 'Sorry, I encountered an error. Please try again.' }]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered a connection error. Please check that the backend is running and try again.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const suggestions = [
    'How can I improve my resume?',
    'What skills should I learn for a senior role?',
    'How do I prepare for technical interviews?',
    'What are the current market trends?',
  ];

  // Real insights from data
  const totalApps = applications.length;
  const interviewCount = applications.filter((a) => a.status === 'interview').length;
  const marketReadiness = resumes.length > 0 ? (interviewCount > 0 ? 'Active' : 'Ready') : 'Not started';

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Career Advisor</h1>
        <p className="mt-2 text-muted-foreground">AI-powered career guidance based on your profile</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat */}
        <div className="lg:col-span-2 bg-card rounded-xl border flex flex-col h-[600px]">
          <div className="p-4 border-b flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="font-semibold">AI Career Advisor</h2>
              <p className="text-xs text-muted-foreground">Personalized to your profile</p>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, i) => (
              <div key={i} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                {msg.role === 'assistant' && (
                  <div className="p-2 bg-primary/10 rounded-lg shrink-0">
                    <Bot className="w-4 h-4 text-primary" />
                  </div>
                )}
                <div className={`max-w-[75%] rounded-xl px-4 py-3 text-sm ${
                  msg.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-secondary'
                }`}>
                  {msg.role === 'assistant' ? (
                    <div className="space-y-1.5">
                      {msg.content
                        .replace(/\*\*(.*?)\*\*/g, '$1')   // strip **bold**
                        .replace(/\*(.*?)\*/g, '$1')        // strip *italic*
                        .replace(/#{1,6}\s/g, '')           // strip headings
                        .split('\n')
                        .filter(line => line.trim())
                        .map((line, j) => (
                          <p key={j} className={
                            /^\d+\./.test(line.trim()) || /^[-•]/.test(line.trim())
                              ? 'pl-3'
                              : ''
                          }>{line}</p>
                        ))
                      }
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
                {msg.role === 'user' && (
                  <div className="p-2 bg-primary/10 rounded-lg shrink-0">
                    <User className="w-4 h-4 text-primary" />
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex items-start gap-3">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Bot className="w-4 h-4 text-primary" />
                </div>
                <div className="bg-secondary rounded-xl px-4 py-3">
                  <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                placeholder="Ask about your career..."
                className="flex-1 px-4 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          <div className="bg-card rounded-xl p-5 border">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4" /> Quick Questions
            </h3>
            <div className="space-y-2">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => { setInput(s); }}
                  className="w-full text-left p-2.5 text-sm rounded-lg bg-secondary/50 hover:bg-secondary transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-card rounded-xl p-5 border">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" /> Your Career Stats
            </h3>
            <div className="space-y-3">
              <div>
                <p className="text-xs text-muted-foreground">Total Applications</p>
                <p className="text-2xl font-bold">{totalApps}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Interviews</p>
                <p className="text-2xl font-bold text-blue-600">{interviewCount}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Resumes Uploaded</p>
                <p className="text-2xl font-bold text-green-600">{resumes.length}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Status</p>
                <p className="text-lg font-semibold text-primary">{marketReadiness}</p>
              </div>
            </div>
          </div>

          <div className="bg-card rounded-xl p-5 border">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Target className="w-4 h-4" /> Quick Actions
            </h3>
            <div className="space-y-2 text-sm">
              <a href="/resume" className="block p-2.5 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors">
                → Upload / Analyze Resume
              </a>
              <a href="/job-analysis" className="block p-2.5 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors">
                → Analyze a Job Description
              </a>
              <a href="/resume-optimizer" className="block p-2.5 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors">
                → Optimize Resume for Job
              </a>
              <a href="/applications" className="block p-2.5 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors">
                → Track Applications
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
