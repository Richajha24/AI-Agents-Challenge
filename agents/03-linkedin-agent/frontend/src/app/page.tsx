'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-warm-ivory">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white bg-opacity-95 backdrop-blur-md z-50 border-b border-soft-beige">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="font-space-grotesk text-2xl font-bold text-forest-green flex items-center gap-2">
            💼 LinkedIn Growth Agent
          </div>
          <div className="flex gap-8 items-center">
            <Link href="/#features" className="text-dark-graphite hover:text-forest-green transition font-medium">Features</Link>
            <Link href="/dashboard" className="btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-36 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <span className="bg-muted-gold bg-opacity-20 text-forest-green text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider mb-6 inline-block">
            Automate Your Personal Brand
          </span>
          <h1 className="text-6xl font-bold mb-6 text-gradient font-space-grotesk leading-tight">
            Build Your Authority on LinkedIn
          </h1>
          <p className="text-xl text-dark-graphite mb-12 opacity-80 max-w-2xl mx-auto leading-relaxed">
            Turn your professional background and career goals into a structured brand positioning, content calendar, and ready-to-publish posts in minutes.
          </p>
          <div className="flex gap-6 justify-center">
            <Link href="/dashboard" className="btn-primary text-lg px-8 py-4">
              Enter Workspace
            </Link>
            <a href="#features" className="btn-secondary text-lg px-8 py-4">
              Explore Features
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6 bg-white border-t border-soft-beige">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4 font-space-grotesk">How We Grow Your Profile</h2>
          <p className="text-center text-dark-graphite opacity-70 mb-16 max-w-xl mx-auto">
            Our pipeline of 5 cooperative AI agents analyzes your profile and prepares your monthly strategy step-by-step.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { emoji: '🔍', title: 'Profile Optimization', desc: 'Score your profile and get keyword-optimized headlines and about rewrites.' },
              { emoji: '🎯', title: 'Brand Positioning', desc: 'Define your professional brand identity, positioning statement, and core pillars.' },
              { emoji: '📅', title: 'Content Strategy', desc: 'Generate a structured weekly content calendar aligned to your brand pillars.' },
              { emoji: '✍️', title: 'Post Generation', desc: 'Get ready-to-publish copy-pasteable posts designed with strong hooks and formatting.' },
              { emoji: '📈', title: 'Growth Roadmap', desc: '30, 60, and 90-day actionable tasks and milestones to track your networking success.' },
            ].map((feature, i) => (
              <div key={i} className="card flex flex-col justify-between">
                <div>
                  <div className="text-3xl mb-4">{feature.emoji}</div>
                  <h3 className="font-space-grotesk font-bold text-xl mb-2 text-forest-green">{feature.title}</h3>
                  <p className="text-sm opacity-70 leading-relaxed">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Steps */}
      <section className="py-20 px-6 bg-warm-ivory border-t border-soft-beige">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16 font-space-grotesk">Process Workflow</h2>
          <div className="space-y-8">
            {[
              { step: '1', title: 'Submit Profile URL & Goals', desc: 'Paste your URL, target industry, and career aspirations into our intake form.' },
              { step: '2', title: 'AI Agent Processing', desc: 'Our sequential pipeline analyzes your data and outputs structured reports.' },
              { step: '3', title: 'Optimize & Publish', desc: 'Implement recommendations, copy posts, and follow your customized 90-day roadmap.' },
            ].map((item, i) => (
              <div key={i} className="flex gap-6 items-start">
                <div className="w-12 h-12 rounded-full bg-forest-green text-white flex items-center justify-center font-bold flex-shrink-0 font-space-grotesk text-lg">
                  {item.step}
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2 font-space-grotesk">{item.title}</h3>
                  <p className="text-dark-graphite opacity-70 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark-graphite text-warm-ivory py-10 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="font-space-grotesk text-xl font-bold">
            💼 LinkedIn Growth Agent
          </div>
          <div className="text-center opacity-70 text-sm">
            <p>&copy; 2026 LinkedIn Growth Agent. Part of the 20-Agent Challenge.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
