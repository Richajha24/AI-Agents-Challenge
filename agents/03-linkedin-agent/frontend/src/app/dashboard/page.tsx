'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface Analysis {
  analysis_id: string
  profile_url: string
  industry: string
  status: string
  created_at: string
  completed_at?: string
}

export default function Dashboard() {
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const res = await api.get('/api/v1/history')
      setAnalyses(res.data)
    } catch (error) {
      console.error(error)
      toast.error('Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-warm-ivory">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="font-space-grotesk text-2xl font-bold text-forest-green flex items-center gap-2">
            💼 LinkedIn Growth Agent
          </Link>
          <div className="font-medium text-dark-graphite text-sm">Dashboard</div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* New Analysis Card */}
        <Link href="/analysis/new">
          <div className="card mb-12 cursor-pointer hover:scale-[1.02] transition duration-300 border-dashed border-2 border-forest-green bg-forest-green bg-opacity-5">
            <div className="text-center">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-2xl font-bold mb-2 font-space-grotesk text-forest-green">New LinkedIn Analysis</h3>
              <p className="text-dark-graphite opacity-70">Analyze a profile, goals, and generate custom brand positioning and content calendars</p>
            </div>
          </div>
        </Link>

        {/* Recent Analyses */}
        <div>
          <h2 className="text-3xl font-bold mb-8 font-space-grotesk text-forest-green">Recent Growth Strategies</h2>
          {loading ? (
            <div className="text-center py-12">
              <p className="text-dark-graphite opacity-70">Loading history...</p>
            </div>
          ) : analyses.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-dark-graphite opacity-70">No strategies generated yet. Submit a profile above to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {analyses.map((analysis) => (
                <Link key={analysis.analysis_id} href={`/report/${analysis.analysis_id}`}>
                  <div className="card cursor-pointer hover:scale-[1.005] transition">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                      <div>
                        <h3 className="text-xl font-bold mb-1 font-space-grotesk text-forest-green truncate max-w-md">{analysis.profile_url}</h3>
                        <p className="text-sm text-dark-graphite opacity-70">{analysis.industry}</p>
                        <p className="text-xs text-dark-graphite opacity-50 mt-2">
                          {new Date(analysis.created_at).toLocaleString()}
                        </p>
                      </div>
                      <span className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider ${
                        analysis.status === 'completed' ? 'bg-success text-white' :
                        analysis.status === 'in_progress' ? 'bg-info text-white' :
                        'bg-soft-beige text-dark-graphite'
                      }`}>
                        {analysis.status}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
