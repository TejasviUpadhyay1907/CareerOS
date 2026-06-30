'use client';

import { Briefcase, FileText, Calendar, CheckCircle, TrendingUp, Target, Bell } from 'lucide-react';
import { useAuth } from '@/components/providers/auth-provider';
import { useResumes } from '@/hooks/api/resume';
import { useApplications, useTasks, useNotifications } from '@/hooks/api/workflow';

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: resumes = [], isLoading: resumesLoading } = useResumes(user?.id ?? '');
  const { data: applications = [], isLoading: appsLoading } = useApplications();
  const { data: tasks = [], isLoading: tasksLoading } = useTasks();
  const { data: notifications = [] } = useNotifications(true);

  const interviewApps = applications.filter((a) => a.status === 'interview');
  const offerApps = applications.filter((a) => a.status === 'offer');
  const pendingTasks = tasks.filter((t) => t.status === 'pending').slice(0, 4);
  const unreadNotifs = notifications.slice(0, 4);

  const loading = resumesLoading || appsLoading || tasksLoading;

  const stats = [
    { label: 'Applications', value: applications.length, icon: Briefcase, color: 'text-blue-600', bg: 'bg-blue-100 dark:bg-blue-900' },
    { label: 'Resumes',      value: resumes.length,       icon: FileText,  color: 'text-green-600', bg: 'bg-green-100 dark:bg-green-900' },
    { label: 'Interviews',   value: interviewApps.length, icon: Calendar,  color: 'text-purple-600', bg: 'bg-purple-100 dark:bg-purple-900' },
    { label: 'Offers',       value: offerApps.length,     icon: CheckCircle, color: 'text-yellow-600', bg: 'bg-yellow-100 dark:bg-yellow-900' },
  ];

  // Stage funnel
  const stageCounts: Record<string, number> = {};
  for (const app of applications) {
    stageCounts[app.status] = (stageCounts[app.status] ?? 0) + 1;
  }
  const funnelStages = [
    { stage: 'Applied',    key: 'applied' },
    { stage: 'Screening',  key: 'preparing' },
    { stage: 'Interview',  key: 'interview' },
    { stage: 'Offer',      key: 'offer' },
  ];
  const maxCount = Math.max(...funnelStages.map((s) => stageCounts[s.key] ?? 0), 1);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">
          {user?.first_name ? `Welcome back, ${user.first_name}` : 'Dashboard'}
        </h1>
        <p className="mt-1 text-muted-foreground">Your career overview</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-card rounded-xl p-6 border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.label}</p>
                <p className="text-3xl font-bold mt-1">
                  {loading ? '—' : stat.value}
                </p>
              </div>
              <div className={`p-3 rounded-lg ${stat.bg}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pending Tasks */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Target className="w-5 h-5" /> Upcoming Tasks
          </h2>
          {pendingTasks.length === 0 ? (
            <p className="text-muted-foreground text-sm">
              {loading ? 'Loading...' : 'No pending tasks. Add tasks from the Applications page.'}
            </p>
          ) : (
            <div className="space-y-3">
              {pendingTasks.map((task) => (
                <div key={task.id} className="flex items-center justify-between p-3 rounded-lg bg-secondary/50">
                  <div className="flex items-center gap-3">
                    <Target className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">{task.title}</p>
                      {task.due_date && (
                        <p className="text-xs text-muted-foreground">
                          Due: {new Date(task.due_date).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    task.priority === 'high' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300' :
                    task.priority === 'medium' ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-300' :
                    'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'
                  }`}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Notifications */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Bell className="w-5 h-5" /> Notifications
          </h2>
          {unreadNotifs.length === 0 ? (
            <p className="text-muted-foreground text-sm">
              {loading ? 'Loading...' : 'No new notifications.'}
            </p>
          ) : (
            <div className="space-y-3">
              {unreadNotifs.map((n) => (
                <div key={n.id} className="flex items-start gap-3 p-3 rounded-lg bg-secondary/50">
                  <div className="w-2 h-2 mt-2 rounded-full bg-primary shrink-0" />
                  <div>
                    <p className="text-sm font-medium">{n.title}</p>
                    <p className="text-xs text-muted-foreground">{n.message}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Application Funnel */}
      <div className="bg-card rounded-xl p-6 border">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" /> Application Pipeline
        </h2>
        {applications.length === 0 ? (
          <p className="text-muted-foreground text-sm">
            {loading ? 'Loading...' : 'No applications yet. Add your first application on the Applications page.'}
          </p>
        ) : (
          <div className="space-y-4">
            {funnelStages.map((item) => {
              const count = stageCounts[item.key] ?? 0;
              const pct = Math.round((count / maxCount) * 100);
              return (
                <div key={item.stage}>
                  <div className="flex justify-between text-sm mb-1.5">
                    <span className="font-medium">{item.stage}</span>
                    <span className="text-muted-foreground">{count} application{count !== 1 ? 's' : ''}</span>
                  </div>
                  <div className="h-2 bg-secondary rounded-full overflow-hidden">
                    <div className="h-full bg-primary transition-all duration-500" style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
