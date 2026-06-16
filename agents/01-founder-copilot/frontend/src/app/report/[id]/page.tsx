'use client'

import { useState, useEffect, useRef } from 'react'
import { useParams } from 'next/navigation'
import api from '@/lib/api'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import toast from 'react-hot-toast'

export default function ReportPage() {
  const params = useParams()
  const analysisId = params?.id as string
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const reportRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadReport()
  }, [analysisId])

  const loadReport = async () => {
    try {
      const res = await api.get(`/api/v1/report/${analysisId}`)
      setReport(res.data)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to load report')
    } finally {
      setLoading(false)
    }
  }

  const exportPDF = async () => {
    if (!reportRef.current) return

    try {
      const canvas = await html2canvas(reportRef.current, { scale: 2 })
      const pdf = new jsPDF('p', 'mm', 'a4')
      const imgData = canvas.toDataURL('image/png')
      const imgWidth = 210
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      
      pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight)
      pdf.save(`startup-analysis-${new Date().toISOString().split('T')[0]}.pdf`)
      toast.success('PDF exported successfully!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-warm-ivory flex items-center justify-center">
        <div className="text-center">
          <p className="text-dark-graphite">Loading report...</p>
        </div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-warm-ivory flex items-center justify-center">
        <div className="text-center">
          <p className="text-dark-graphite">Report not found</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-warm-ivory">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <a href="/" className="font-space-grotesk text-2xl font-bold text-forest-green">
            Founder Copilot
          </a>
          <div className="flex gap-4">
            <button onClick={exportPDF} className="btn-secondary">
              Export PDF
            </button>
            <a href="/dashboard" className="btn-primary">
              Back to Dashboard
            </a>
          </div>
        </div>
      </nav>

      <div ref={reportRef} className="max-w-4xl mx-auto px-6 py-12">
        {/* Report Header */}
        <div className="mb-12 pb-8 border-b border-soft-beige">
          <h1 className="text-5xl font-bold mb-4 text-gradient">{report.startup_idea}</h1>
          <p className="text-lg text-dark-graphite opacity-70">{report.industry}</p>
          <p className="text-sm text-dark-graphite opacity-50 mt-4">
            Generated on {new Date(report.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Idea Analysis Section */}
        {report.idea_analysis && (
          <ReportSection title="Idea Analysis" data={report.idea_analysis} />
        )}

        {/* Competitor Analysis Section */}
        {report.competitor_analysis && (
          <ReportSection title="Competitor Analysis" data={report.competitor_analysis} />
        )}

        {/* Market Research Section */}
        {report.market_research && (
          <ReportSection title="Market Research" data={report.market_research} />
        )}

        {/* Customer Personas Section */}
        {report.customer_personas && (
          <ReportSection title="Customer Personas" data={report.customer_personas} />
        )}

        {/* MVP Plan Section */}
        {report.mvp_plan && (
          <ReportSection title="MVP Plan" data={report.mvp_plan} />
        )}

        {/* Pricing Strategy Section */}
        {report.pricing_strategy && (
          <ReportSection title="Pricing Strategy" data={report.pricing_strategy} />
        )}

        {/* Go-To-Market Section */}
        {report.go_to_market && (
          <ReportSection title="Go-To-Market Strategy" data={report.go_to_market} />
        )}

        {/* Execution Roadmap Section */}
        {report.execution_roadmap && (
          <ReportSection title="Execution Roadmap" data={report.execution_roadmap} />
        )}
      </div>
    </div>
  )
}

function ReportSection({ title, data }: { title: string; data: any }) {
  return (
    <div className="mb-12 pb-8 border-b border-soft-beige">
      <h2 className="text-3xl font-bold mb-6 text-forest-green">{title}</h2>
      <div className="prose prose-invert">
        <JsonDisplay data={data} />
      </div>
    </div>
  )
}

function JsonDisplay({ data }: { data: any }): JSX.Element {
  if (typeof data === 'string') {
    return <p className="text-dark-graphite opacity-80">{data}</p>
  }

  if (Array.isArray(data)) {
    return (
      <ul className="list-disc list-inside space-y-2">
        {data.map((item, idx) => (
          <li key={idx} className="text-dark-graphite opacity-80">
            {typeof item === 'object' ? JSON.stringify(item) : item}
          </li>
        ))}
      </ul>
    )
  }

  if (typeof data === 'object' && data !== null) {
    return (
      <div className="space-y-4">
        {Object.entries(data).map(([key, value]) => (
          <div key={key}>
            <h4 className="font-bold text-forest-green mb-2 capitalize">{key}</h4>
            <div className="ml-4 text-dark-graphite opacity-80">
              <JsonDisplay data={value} />
            </div>
          </div>
        ))}
      </div>
    )
  }

  return <span className="text-dark-graphite opacity-80">{String(data)}</span>
}
