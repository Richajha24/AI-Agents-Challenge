'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'

export default function AnalysisWorkspace() {
  const params = useParams()
  const analysisId = params?.id as string
  const [status, setStatus] = useState('pending')
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (!analysisId) return

    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/api/v1/analysis/${analysisId}`)
        setStatus(res.data.status)
        setProgress(res.data.progress)

        if (res.data.status === 'completed') {
          clearInterval(interval)
          window.location.href = `/report/${analysisId}`
        }
      } catch (error) {
        console.error(error)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [analysisId])

  const steps = [
    'Profile Optimization',
    'Personal Brand Strategy',
    'Content Strategy & Calendar',
    'Ready-to-Publish Post Generation',
    'Growth Roadmap & Milestones',
  ]

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
        <h1 className="text-4xl font-bold mb-2 font-space-grotesk text-forest-green">Assembling Strategy</h1>
        <p className="text-dark-graphite opacity-70 mb-12">
          Our AI branding agents are coordinating your LinkedIn growth deliverables. This typically takes 1-2 minutes.
        </p>

        {/* Progress Bar */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-4">
            <span className="text-sm font-bold">Pipeline Progress</span>
            <span className="text-sm font-bold">{progress}%</span>
          </div>
          <div className="w-full bg-soft-beige rounded-full h-2">
            <div
              className="bg-forest-green h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Steps */}
        <div className="space-y-4">
          {steps.map((step, idx) => {
            const stepProgress = (idx + 1) * (100 / steps.length)
            const isActive = progress >= stepProgress - 5
            const isCompleted = progress > stepProgress

            return (
              <div key={idx} className="flex items-start gap-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 font-bold text-sm ${
                  isCompleted ? 'bg-success text-white' :
                  isActive ? 'bg-forest-green text-warm-ivory' :
                  'bg-soft-beige text-dark-graphite'
                }`}>
                  {isCompleted ? '✓' : idx + 1}
                </div>
                <div>
                  <p className={`font-semibold ${isActive ? 'text-forest-green' : 'text-dark-graphite opacity-50'}`}>
                    {step}
                  </p>
                  {isActive && !isCompleted && (
                    <p className="text-sm text-dark-graphite opacity-70 mt-1">In progress...</p>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <div className="mt-12 text-center">
          <p className="text-dark-graphite opacity-70">
            ✨ Please wait, you will be automatically redirected to your finished growth report
          </p>
        </div>
      </div>
    </div>
  )
}
