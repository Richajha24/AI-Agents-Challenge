'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'
import toast from 'react-hot-toast'

export default function NewAnalysis() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    startup_idea: '',
    industry: '',
    problem_statement: '',
    website_url: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.startup_idea || !formData.industry || !formData.problem_statement) {
      toast.error('Please fill in all required fields')
      return
    }

    setLoading(true)
    try {
      const res = await api.post('/api/v1/analyze', formData)
      const analysisId = res.data.analysis_id
      router.push(`/analysis/${analysisId}`)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to start analysis')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-warm-ivory">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/dashboard" className="font-space-grotesk text-2xl font-bold text-forest-green">
            Founder Copilot
          </a>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-2">Analyze Your Startup Idea</h1>
        <p className="text-dark-graphite opacity-70 mb-12">
          Tell us about your startup concept and we'll provide comprehensive market analysis, competitor research, and an execution roadmap.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Startup Idea */}
          <div>
            <label className="block text-sm font-bold mb-2">Startup Idea *</label>
            <input
              type="text"
              name="startup_idea"
              value={formData.startup_idea}
              onChange={handleChange}
              placeholder="e.g., AI platform that helps students find internships"
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Industry */}
          <div>
            <label className="block text-sm font-bold mb-2">Industry *</label>
            <select
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            >
              <option value="">Select an industry</option>
              <option value="EdTech">EdTech</option>
              <option value="FinTech">FinTech</option>
              <option value="HealthTech">HealthTech</option>
              <option value="SaaS">SaaS</option>
              <option value="E-commerce">E-commerce</option>
              <option value="AI/ML">AI/ML</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {/* Problem Statement */}
          <div>
            <label className="block text-sm font-bold mb-2">Problem Statement *</label>
            <textarea
              name="problem_statement"
              value={formData.problem_statement}
              onChange={handleChange}
              placeholder="Describe the problem your startup solves..."
              rows={5}
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Website URL (Optional) */}
          <div>
            <label className="block text-sm font-bold mb-2">Website URL (Optional)</label>
            <input
              type="url"
              name="website_url"
              value={formData.website_url}
              onChange={handleChange}
              placeholder="https://yourwebsite.com"
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-4 pt-6">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Starting Analysis...' : 'Start Analysis'}
            </button>
            <a href="/dashboard" className="btn-secondary flex-1 text-center">
              Cancel
            </a>
          </div>
        </form>
      </div>
    </div>
  )
}
