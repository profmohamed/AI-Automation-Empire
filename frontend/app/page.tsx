'use client';

import { useState } from 'react';

export default function Home() {
  const [stats] = useState({
    opportunities: 1247,
    proposals: 89,
    campaigns: 12,
    success_rate: 67,
  });

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🤖 AI Automation Empire
          </h1>
          <p className="text-xl text-gray-600">
            The Ultimate Web Scraping & Opportunity Engine
          </p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <StatCard title="Opportunities" value={stats.opportunities} icon="📊" />
          <StatCard title="Proposals Sent" value={stats.proposals} icon="📝" />
          <StatCard title="Active Campaigns" value={stats.campaigns} icon="🚀" />
          <StatCard title="Success Rate" value={`${stats.success_rate}%`} icon="✨" />
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            title="Smart Scraping"
            description="Scrape jobs from Upwork, LinkedIn, Indeed, and more with AI-powered anti-bot protection"
            icon="🕷️"
          />
          <FeatureCard
            title="AI Analysis"
            description="Automatically analyze, score, and categorize opportunities using advanced AI"
            icon="🧠"
          />
          <FeatureCard
            title="Auto Proposals"
            description="Generate personalized, winning proposals in seconds with AI"
            icon="✍️"
          />
          <FeatureCard
            title="Multi-Channel Outreach"
            description="Automate outreach via Email, WhatsApp, LinkedIn, and Telegram"
            icon="📧"
          />
          <FeatureCard
            title="Autonomous Agent"
            description="24/7 automated loop: scrape → analyze → contact → follow-up"
            icon="🤖"
          />
          <FeatureCard
            title="Real-Time Dashboard"
            description="Monitor everything in real-time with beautiful analytics"
            icon="📈"
          />
        </div>

        {/* CTA Section */}
        <div className="mt-12 bg-white rounded-2xl shadow-xl p-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Build Your Empire?</h2>
          <p className="text-gray-600 mb-6">
            Start automating your freelance business today
          </p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold text-lg transition">
            Get Started →
          </button>
        </div>
      </div>
    </main>
  );
}

function StatCard({ title, value, icon }: { title: string; value: string | number; icon: string }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-3xl font-bold text-gray-900">{value}</div>
      <div className="text-gray-600">{title}</div>
    </div>
  );
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
