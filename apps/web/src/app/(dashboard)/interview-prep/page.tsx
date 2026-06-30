'use client';

import { useState, useEffect, useRef } from 'react';
import { Play, Mic, StopCircle, BookOpen, Target, CheckCircle, Clock, Loader2, Volume2 } from 'lucide-react';
import { useApplications } from '@/hooks/api/workflow';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Question {
  id: number;
  question: string;
  hint?: string;
}

const QUESTION_BANK: Record<string, Question[]> = {
  technical: [
    { id: 1, question: 'Explain the difference between == and === in JavaScript.', hint: 'Think about type coercion' },
    { id: 2, question: 'What is the virtual DOM and how does React use it?', hint: 'Reconciliation algorithm' },
    { id: 3, question: 'Explain event bubbling and how to stop it.', hint: 'stopPropagation vs preventDefault' },
    { id: 4, question: 'What are React hooks and why were they introduced?', hint: 'Class component problems' },
    { id: 5, question: 'Explain closures in JavaScript with an example.', hint: 'Lexical scoping' },
  ],
  behavioral: [
    { id: 1, question: 'Tell me about a time you had to handle a difficult team member.', hint: 'Use STAR method' },
    { id: 2, question: 'Describe a project you failed at and what you learned.', hint: 'Show growth mindset' },
    { id: 3, question: 'How do you handle tight deadlines?', hint: 'Prioritization and communication' },
    { id: 4, question: 'Tell me about a time you had to learn a new technology quickly.', hint: 'Be specific with outcomes' },
  ],
  system: [
    { id: 1, question: 'Design a URL shortening service like bit.ly.', hint: 'Consider scale: 100M URLs' },
    { id: 2, question: 'Design a real-time chat application.', hint: 'WebSockets, message queues' },
    { id: 3, question: 'Design a distributed file storage system.', hint: 'Sharding, replication' },
  ],
  company: [
    { id: 1, question: 'Why do you want to work at our company?', hint: 'Research the company first' },
    { id: 2, question: 'Where do you see yourself in 5 years?', hint: 'Align with company growth' },
    { id: 3, question: 'What questions do you have for us?', hint: 'Ask about team, growth, challenges' },
  ],
};

const CATEGORIES = [
  { id: 'technical', name: 'Technical', icon: '💻', count: 5 },
  { id: 'behavioral', name: 'Behavioral', icon: '🎯', count: 4 },
  { id: 'system', name: 'System Design', icon: '🏗️', count: 3 },
  { id: 'company', name: 'Company Specific', icon: '🏢', count: 3 },
];

export default function InterviewPrepPage() {
  const { data: applications = [] } = useApplications();
  const interviewApps = applications.filter((a) => a.status === 'interview');

  const [category, setCategory] = useState('technical');
  const [idx, setIdx] = useState(0);
  const [answered, setAnswered] = useState<Set<number>>(new Set());
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [feedback, setFeedback] = useState('');
  const [loadingFeedback, setLoadingFeedback] = useState(false);
  const [showGoalModal, setShowGoalModal] = useState(false);
  const [goal, setGoal] = useState('');
  const [goals, setGoals] = useState<string[]>([]);
  const [mockMode, setMockMode] = useState(false);
  const [mockMessages, setMockMessages] = useState<{role:string;content:string}[]>([]);
  const [mockInput, setMockInput] = useState('');
  const [mockLoading, setMockLoading] = useState(false);

  const recognitionRef = useRef<any>(null);

  const questions = QUESTION_BANK[category] ?? [];
  const currentQ = questions[idx];

  // Load goals from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('careeros_interview_goals');
    if (saved) setGoals(JSON.parse(saved));
  }, []);

  const saveGoal = () => {
    if (!goal.trim()) return;
    const updated = [...goals, goal.trim()];
    setGoals(updated);
    localStorage.setItem('careeros_interview_goals', JSON.stringify(updated));
    setGoal('');
    setShowGoalModal(false);
  };

  // Progress per category
  const getProgress = (cat: string) => {
    const key = `careeros_progress_${cat}`;
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) as number[] : [];
  };

  const markAnswered = () => {
    const newSet = new Set(answered).add(currentQ.id);
    setAnswered(newSet);
    // Persist
    const key = `careeros_progress_${category}`;
    const existing = getProgress(category);
    if (!existing.includes(currentQ.id)) {
      localStorage.setItem(key, JSON.stringify([...existing, currentQ.id]));
    }
  };

  const startRecording = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition not supported in this browser. Use Chrome for best experience.');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    recognition.onresult = (event: any) => {
      let final = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) final += event.results[i][0].transcript + ' ';
      }
      if (final) setTranscript((prev) => prev + final);
    };
    recognition.start();
    recognitionRef.current = recognition;
    setRecording(true);
    setTranscript('');
    setFeedback('');
  };

  const stopRecording = async () => {
    recognitionRef.current?.stop();
    setRecording(false);
    if (transcript) {
      await getAIFeedback(transcript);
    }
  };

  const getAIFeedback = async (answer: string) => {
    setLoadingFeedback(true);
    try {
      const token = localStorage.getItem('careeros_token');
      const res = await fetch(`${API_BASE}/api/v1/career/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          messages: [
            {
              role: 'user',
              content: `Interview question: "${currentQ.question}"\n\nMy answer: "${answer}"\n\nPlease provide specific, constructive feedback on my answer. Rate it 1-10 and suggest improvements. Be concise (3-5 sentences).`,
            },
          ],
          context: `Category: ${category} interview questions`,
        }),
      });
      if (res.ok) {
        const data = await res.json() as { reply: string };
        setFeedback(data.reply);
      }
    } catch {
      setFeedback('Configure OPENAI_API_KEY to get AI feedback on your answers.');
    } finally {
      setLoadingFeedback(false);
    }
  };

  const startMockInterview = async () => {
    setMockMode(true);
    setMockMessages([]);
    const token = localStorage.getItem('careeros_token');
    setMockLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/career/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          messages: [{ role: 'user', content: `Start a mock interview for ${category} questions. Ask me the first question and then evaluate my answers one by one.` }],
          context: `Mock interview mode. Category: ${category}.`,
        }),
      });
      if (res.ok) {
        const data = await res.json() as { reply: string };
        setMockMessages([
          { role: 'assistant', content: data.reply },
        ]);
      }
    } catch {
      setMockMessages([{ role: 'assistant', content: 'Set OPENAI_API_KEY to enable mock interview AI.' }]);
    } finally {
      setMockLoading(false);
    }
  };

  const sendMockAnswer = async () => {
    if (!mockInput.trim()) return;
    const updated = [...mockMessages, { role: 'user', content: mockInput }];
    setMockMessages(updated);
    setMockInput('');
    setMockLoading(true);
    try {
      const token = localStorage.getItem('careeros_token');
      const res = await fetch(`${API_BASE}/api/v1/career/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          messages: updated,
          context: `Mock interview. Category: ${category}.`,
        }),
      });
      if (res.ok) {
        const data = await res.json() as { reply: string };
        setMockMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
      }
    } catch {} finally {
      setMockLoading(false);
    }
  };

  if (mockMode) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Mock Interview</h1>
            <p className="text-muted-foreground mt-1 capitalize">{category} questions — AI Interviewer</p>
          </div>
          <button onClick={() => setMockMode(false)} className="px-4 py-2 border rounded-lg text-sm hover:bg-secondary">
            Exit Mock
          </button>
        </div>
        <div className="bg-card rounded-xl border flex flex-col h-[500px]">
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {mockMessages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-xl px-4 py-3 text-sm ${
                  m.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary'
                }`}>{m.content}</div>
              </div>
            ))}
            {mockLoading && (
              <div className="flex justify-start">
                <div className="bg-secondary rounded-xl px-4 py-3">
                  <Loader2 className="w-4 h-4 animate-spin" />
                </div>
              </div>
            )}
          </div>
          <div className="p-4 border-t flex gap-2">
            <input
              value={mockInput}
              onChange={(e) => setMockInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMockAnswer()}
              placeholder="Type your answer..."
              className="flex-1 px-3 py-2 border rounded-lg bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              onClick={sendMockAnswer}
              disabled={mockLoading}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Interview Preparation</h1>
        <p className="mt-2 text-muted-foreground">Practice questions and get AI feedback on your answers</p>
      </div>

      {showGoalModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-card rounded-2xl p-6 w-full max-w-sm border shadow-xl">
            <h2 className="font-semibold mb-4">Set Practice Goal</h2>
            <input
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="e.g. Practice 5 behavioral questions today"
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary mb-4"
            />
            <div className="flex gap-3">
              <button onClick={() => setShowGoalModal(false)} className="flex-1 py-2 border rounded-lg text-sm">Cancel</button>
              <button onClick={saveGoal} className="flex-1 py-2 bg-primary text-primary-foreground rounded-lg text-sm">Save Goal</button>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Category */}
          <div className="bg-card rounded-xl p-6 border">
            <h2 className="font-semibold mb-4">Select Category</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {CATEGORIES.map((cat) => {
                const done = getProgress(cat.id).length;
                return (
                  <button
                    key={cat.id}
                    onClick={() => { setCategory(cat.id); setIdx(0); setTranscript(''); setFeedback(''); }}
                    className={`p-4 rounded-lg border-2 transition-colors text-left ${
                      category === cat.id ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
                    }`}
                  >
                    <div className="text-2xl mb-2">{cat.icon}</div>
                    <p className="font-medium text-sm">{cat.name}</p>
                    <p className="text-xs text-muted-foreground mt-1">{done}/{cat.count} done</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Question */}
          {currentQ && (
            <div className="bg-card rounded-xl p-6 border space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold">Question {idx + 1} of {questions.length}</h2>
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" /> 2 min suggested
                </span>
              </div>

              <div className="bg-secondary/50 rounded-lg p-5">
                <p className="text-base">{currentQ.question}</p>
                {currentQ.hint && (
                  <p className="text-xs text-muted-foreground mt-2">💡 Hint: {currentQ.hint}</p>
                )}
              </div>

              {/* Recording */}
              <div className="flex items-center gap-3 flex-wrap">
                <button
                  onClick={idx > 0 ? () => { setIdx(idx - 1); setTranscript(''); setFeedback(''); } : undefined}
                  disabled={idx === 0}
                  className="px-4 py-2 border rounded-lg text-sm hover:bg-secondary disabled:opacity-30 transition-colors"
                >
                  Previous
                </button>

                {!recording ? (
                  <button
                    onClick={startRecording}
                    className="flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
                  >
                    <Mic className="w-4 h-4" /> Record Answer
                  </button>
                ) : (
                  <button
                    onClick={stopRecording}
                    className="flex items-center gap-2 px-6 py-2.5 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 animate-pulse transition-colors"
                  >
                    <StopCircle className="w-4 h-4" /> Stop Recording
                  </button>
                )}

                <button
                  onClick={markAnswered}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm transition-colors ${
                    answered.has(currentQ.id)
                      ? 'bg-green-500 text-white'
                      : 'bg-secondary hover:bg-secondary/80'
                  }`}
                >
                  <CheckCircle className="w-4 h-4" />
                  {answered.has(currentQ.id) ? 'Answered ✓' : 'Mark Answered'}
                </button>

                <button
                  onClick={idx < questions.length - 1 ? () => { setIdx(idx + 1); setTranscript(''); setFeedback(''); } : undefined}
                  disabled={idx === questions.length - 1}
                  className="px-4 py-2 border rounded-lg text-sm hover:bg-secondary disabled:opacity-30 transition-colors ml-auto"
                >
                  Next
                </button>
              </div>

              {/* Transcript */}
              {transcript && (
                <div className="bg-blue-50 dark:bg-blue-950 rounded-lg p-4">
                  <p className="text-xs font-medium text-blue-700 dark:text-blue-300 mb-1 flex items-center gap-1">
                    <Volume2 className="w-3.5 h-3.5" /> Your Answer (transcribed)
                  </p>
                  <p className="text-sm">{transcript}</p>
                </div>
              )}

              {/* AI Feedback */}
              {loadingFeedback && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="w-4 h-4 animate-spin" /> Getting AI feedback...
                </div>
              )}
              {feedback && !loadingFeedback && (
                <div className="bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg p-4">
                  <p className="text-xs font-medium text-green-700 dark:text-green-300 mb-2">🤖 AI Feedback</p>
                  <p className="text-sm">{feedback}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          <div className="bg-card rounded-xl p-5 border">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Target className="w-4 h-4" /> Your Progress
            </h3>
            <div className="space-y-3">
              {CATEGORIES.map((cat) => {
                const done = getProgress(cat.id).length;
                const pct = Math.round((done / cat.count) * 100);
                return (
                  <div key={cat.id}>
                    <div className="flex justify-between text-xs mb-1">
                      <span>{cat.name}</span>
                      <span className="text-muted-foreground">{done}/{cat.count}</span>
                    </div>
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                      <div className="h-full bg-primary transition-all" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {interviewApps.length > 0 && (
            <div className="bg-card rounded-xl p-5 border">
              <h3 className="font-semibold mb-3">Upcoming Interviews</h3>
              <div className="space-y-2">
                {interviewApps.slice(0, 3).map((app) => (
                  <div key={app.id} className="p-3 rounded-lg bg-secondary/50 text-sm">
                    <p className="font-medium">Application #{app.id.toString().slice(0, 8)}</p>
                    <p className="text-xs text-primary mt-1">Status: interview stage</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {goals.length > 0 && (
            <div className="bg-card rounded-xl p-5 border">
              <h3 className="font-semibold mb-3">Practice Goals</h3>
              <ul className="space-y-2">
                {goals.map((g, i) => (
                  <li key={i} className="text-sm flex items-start gap-2">
                    <CheckCircle className="w-3.5 h-3.5 text-primary mt-0.5 shrink-0" />
                    {g}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="bg-card rounded-xl p-5 border">
            <h3 className="font-semibold mb-3">Quick Actions</h3>
            <div className="space-y-2">
              <button
                onClick={startMockInterview}
                className="w-full text-left p-2.5 text-sm rounded-lg bg-secondary/50 hover:bg-secondary transition-colors flex items-center gap-2"
              >
                <Play className="w-4 h-4" /> Start Mock Interview
              </button>
              <a
                href="https://leetcode.com"
                target="_blank"
                rel="noopener noreferrer"
                className="block p-2.5 text-sm rounded-lg bg-secondary/50 hover:bg-secondary transition-colors"
              >
                <span className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4" /> View Study Materials
                </span>
              </a>
              <button
                onClick={() => setShowGoalModal(true)}
                className="w-full text-left p-2.5 text-sm rounded-lg bg-secondary/50 hover:bg-secondary transition-colors flex items-center gap-2"
              >
                <Target className="w-4 h-4" /> Set Practice Goals
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
