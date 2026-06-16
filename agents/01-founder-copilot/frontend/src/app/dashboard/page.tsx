'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface Analysis {
  analysis_id: string
  startup_idea: string
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
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-warm-ivory">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="font-space-grotesk text-2xl font-bold text-forest-green">
            Founder Copilot
          </Link>
          <div>Dashboard</div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* New Analysis Card */}
        <Link href="/analysis/new">
          <div className="card mb-12 cursor-pointer hover:scale-105 transition">
            <div className="text-center">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-2xl font-bold mb-2">New Analysis</h3>
              <p className="text-dark-graphite opacity-70">Start analyzing a new startup idea</p>
            </div>
          </div>
        </Link>

        {/* Recent Analyses */}
        <div>
          <h2 className="text-3xl font-bold mb-8">Recent Analyses</h2>
          {loading ? (
            <div className="text-center py-12">
              <p className="text-dark-graphite opacity-70">Loading...</p>
            </div>
          ) : analyses.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-dark-graphite opacity-70">No analyses yet. Start with a new one!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {analyses.map((analysis) => (
                <Link key={analysis.analysis_id} href={`/report/${analysis.analysis_id}`}>
                  <div className="card cursor-pointer">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-xl font-bold mb-2">{analysis.startup_idea}</h3>
                        <p className="text-sm text-dark-graphite opacity-70">{analysis.industry}</p>
                        <p className="text-xs text-dark-graphite opacity-50 mt-2">
                          {new Date(analysis.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <span className={`px-4 py-2 rounded-full text-sm font-bold ${analysis.status === 'completed' ? 'bg-success text-white' :
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
