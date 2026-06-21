'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import toast from 'react-hot-toast'

export default function NewAnalysis() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    profile_url: '',
    profile_info: '',
    industry: '',
    career_goals: '',
    target_audience: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.profile_url || !formData.industry || !formData.career_goals || !formData.target_audience) {
      toast.error('Please fill in all required fields')
      return
    }

    setLoading(true)
    try {
      const res = await api.post('/api/v1/profile/analyze', formData)
      const analysisId = res.data.analysis_id
      router.push(`/analysis/${analysisId}`)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to start analysis')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-warm-ivory font-manrope">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <Link href="/dashboard" className="font-space-grotesk text-2xl font-bold text-forest-green flex items-center gap-2">
            💼 LinkedIn Growth Agent
          </Link>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-2 font-space-grotesk text-forest-green">Personal Branding Intake</h1>
        <p className="text-dark-graphite opacity-70 mb-12">
          Submit your LinkedIn profile data and objectives. Our sequential agent pipeline will prepare a comprehensive brand strategy and content plan.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Profile URL */}
          <div>
            <label className="block text-sm font-bold mb-2">LinkedIn Profile URL *</label>
            <input
              type="url"
              name="profile_url"
              value={formData.profile_url}
              onChange={handleChange}
              placeholder="e.g., https://www.linkedin.com/in/username"
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Copy-paste details */}
          <div>
            <label className="block text-sm font-bold mb-2">Copy-Pasted Biography / Experience (Optional)</label>
            <textarea
              name="profile_info"
              value={formData.profile_info}
              onChange={handleChange}
              placeholder="Copy and paste your current LinkedIn 'About' section or key resume highlights to help the AI refine recommendations..."
              rows={4}
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
            />
          </div>

          {/* Industry */}
          <div>
            <label className="block text-sm font-bold mb-2">Target Industry *</label>
            <input
              type="text"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              placeholder="e.g., Tech / Artificial Intelligence, FinTech, Creative Writing"
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Career Goals */}
          <div>
            <label className="block text-sm font-bold mb-2">Career Goals *</label>
            <textarea
              name="career_goals"
              value={formData.career_goals}
              onChange={handleChange}
              placeholder="What are your goals on LinkedIn? (e.g., land a remote job, attract freelance clients, establish thought leadership...)"
              rows={3}
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Target Audience */}
          <div>
            <label className="block text-sm font-bold mb-2">Target Audience *</label>
            <input
              type="text"
              name="target_audience"
              value={formData.target_audience}
              onChange={handleChange}
              placeholder="e.g., Engineering leaders, recruiters, startup founders"
              className="w-full px-4 py-3 border border-soft-beige rounded-lg focus:outline-none focus:border-forest-green"
              required
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-4 pt-6">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing Profile...' : 'Begin Strategy Run'}
            </button>
            <Link href="/dashboard" className="btn-secondary flex-1 text-center">
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
