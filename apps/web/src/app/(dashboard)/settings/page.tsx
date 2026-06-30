'use client';

import { useState, useEffect } from 'react';
import { User, Bell, Shield, Palette, Save, Loader2, CheckCircle } from 'lucide-react';
import { useAuth } from '@/components/providers/auth-provider';
import apiClient from '@/lib/api-client';

export default function SettingsPage() {
  const { user } = useAuth();
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  // Profile fields
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName]   = useState('');
  const [email, setEmail]         = useState('');

  // Notifications (stored in localStorage for now)
  const [emailNotifs, setEmailNotifs]    = useState(true);
  const [pushNotifs, setPushNotifs]      = useState(true);
  const [weeklyReport, setWeeklyReport]  = useState(false);
  const [statusUpdates, setStatusUpdates] = useState(true);

  // Privacy
  const [profileVisible, setProfileVisible]     = useState(true);
  const [shareAnon, setShareAnon]               = useState(false);
  const [twoFactor, setTwoFactor]               = useState(false);

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name ?? '');
      setLastName(user.last_name ?? '');
      setEmail(user.email);
    }
    // Load saved prefs from localStorage
    const prefs = localStorage.getItem('careeros_prefs');
    if (prefs) {
      try {
        const p = JSON.parse(prefs);
        setEmailNotifs(p.emailNotifs ?? true);
        setPushNotifs(p.pushNotifs ?? true);
        setWeeklyReport(p.weeklyReport ?? false);
        setStatusUpdates(p.statusUpdates ?? true);
        setProfileVisible(p.profileVisible ?? true);
        setShareAnon(p.shareAnon ?? false);
        setTwoFactor(p.twoFactor ?? false);
      } catch {}
    }
  }, [user]);

  const handleSave = async () => {
    setSaving(true);
    setError('');
    try {
      // Save preferences locally
      localStorage.setItem('careeros_prefs', JSON.stringify({
        emailNotifs, pushNotifs, weeklyReport, statusUpdates,
        profileVisible, shareAnon, twoFactor,
      }));

      // In production this would PATCH /api/v1/auth/me — backend endpoint TBD
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError('Failed to save settings. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-2 text-muted-foreground">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <User className="w-4 h-4" /> Profile Settings
          </h2>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-sm font-medium mb-1 block">First Name</label>
                <input
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-1 block">Last Name</label>
                <input
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">Subscription</label>
              <div className="px-3 py-2 border rounded-lg bg-secondary/50 text-sm capitalize">
                {user?.subscription_tier ?? 'free'} plan
              </div>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Bell className="w-4 h-4" /> Notifications
          </h2>
          <div className="space-y-4">
            {[
              { label: 'Email notifications for new job matches',    value: emailNotifs,    set: setEmailNotifs },
              { label: 'Push notifications for interview reminders', value: pushNotifs,     set: setPushNotifs },
              { label: 'Weekly career progress reports',             value: weeklyReport,   set: setWeeklyReport },
              { label: 'Application status updates',                 value: statusUpdates,  set: setStatusUpdates },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between">
                <span className="text-sm">{item.label}</span>
                <button
                  onClick={() => item.set(!item.value)}
                  className={`relative w-10 h-6 rounded-full transition-colors ${
                    item.value ? 'bg-primary' : 'bg-secondary'
                  }`}
                >
                  <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform shadow ${
                    item.value ? 'translate-x-5' : 'translate-x-1'
                  }`} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Privacy */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Shield className="w-4 h-4" /> Privacy
          </h2>
          <div className="space-y-4">
            {[
              { label: 'Make profile visible to recruiters', value: profileVisible, set: setProfileVisible },
              { label: 'Share anonymous usage data',         value: shareAnon,      set: setShareAnon },
              { label: 'Enable two-factor authentication',   value: twoFactor,      set: setTwoFactor },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between">
                <span className="text-sm">{item.label}</span>
                <button
                  onClick={() => item.set(!item.value)}
                  className={`relative w-10 h-6 rounded-full transition-colors ${
                    item.value ? 'bg-primary' : 'bg-secondary'
                  }`}
                >
                  <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform shadow ${
                    item.value ? 'translate-x-5' : 'translate-x-1'
                  }`} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Appearance */}
        <div className="bg-card rounded-xl p-6 border">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Palette className="w-4 h-4" /> Appearance
          </h2>
          <p className="text-sm text-muted-foreground mb-4">
            Use the Dark mode button in the sidebar to switch themes.
          </p>
          <div>
            <label className="text-sm font-medium mb-1 block">Language</label>
            <select className="w-full px-3 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary text-sm">
              <option>English</option>
            </select>
          </div>
        </div>
      </div>

      {error && (
        <p className="text-sm text-destructive bg-destructive/10 px-4 py-2 rounded-lg">{error}</p>
      )}

      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 font-medium transition-colors"
        >
          {saving ? <Loader2 className="w-4 h-4 animate-spin" /> :
           saved  ? <CheckCircle className="w-4 h-4" /> :
                    <Save className="w-4 h-4" />}
          {saved ? 'Saved!' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
}
