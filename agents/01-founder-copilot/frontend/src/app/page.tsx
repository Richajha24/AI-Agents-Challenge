'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white bg-opacity-95 backdrop-blur-md z-50 border-b border-soft-beige">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="font-space-grotesk text-2xl font-bold text-forest-green">
            Founder Copilot
          </div>
          <div className="flex gap-8 items-center">
            <Link href="/#features" className="text-dark-graphite hover:text-forest-green transition">Features</Link>
            <Link href="/dashboard" className="btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold mb-6 text-gradient">
            Your AI Startup Advisor
          </h1>
          <p className="text-xl text-dark-graphite mb-12 opacity-80">
            Turn your startup idea into a complete business analysis in minutes. Get market insights, competitor research, MVP plans, and execution roadmaps—all powered by AI.
          </p>
          <div className="flex gap-6 justify-center">
            <Link href="/dashboard" className="btn-primary text-lg px-8 py-4">
              Start Analysis
            </Link>
            <button className="btn-secondary text-lg px-8 py-4">
              Watch Demo
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">Comprehensive Analysis</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: 'Idea Analysis', desc: 'Validate your startup concept' },
              { title: 'Market Research', desc: 'Understand TAM, SAM, SOM' },
              { title: 'Competitor Analysis', desc: 'Know your competition' },
              { title: 'Customer Personas', desc: 'Define your target users' },
              { title: 'MVP Planning', desc: 'Prioritize core features' },
              { title: 'Pricing Strategy', desc: 'Find optimal pricing models' },
              { title: 'Go-To-Market', desc: 'Launch with confidence' },
              { title: 'Execution Roadmap', desc: '30/60/90 day plans' },
            ].map((feature, i) => (
              <div key={i} className="card">
                <h3 className="font-space-grotesk font-bold mb-2">{feature.title}</h3>
                <p className="text-sm opacity-70">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo Workflow */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">How It Works</h2>
          <div className="space-y-8">
            {[
              { step: '1', title: 'Enter Your Idea', desc: 'Tell us about your startup concept and target market' },
              { step: '2', title: 'AI Analyzes', desc: 'Our agents perform comprehensive research in real-time' },
              { step: '3', title: 'Get Report', desc: 'Receive a professional consulting-grade analysis report' },
            ].map((item, i) => (
              <div key={i} className="flex gap-6 items-start">
                <div className="w-12 h-12 rounded-full bg-forest-green text-white flex items-center justify-center font-bold flex-shrink-0">
                  {item.step}
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                  <p className="text-dark-graphite opacity-70">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-forest-green text-warm-ivory">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Analyze Your Startup?</h2>
          <p className="text-lg mb-8 opacity-90">Get a complete startup analysis in 2-3 minutes.</p>
          <Link href="/dashboard" className="btn-primary bg-warm-ivory text-forest-green">
            Start Free Analysis
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark-graphite text-warm-ivory py-8 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center opacity-70">
            <p>&copy; 2024 Founder Copilot. Built for founders, by founders.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
