'use client'

import { useState, useEffect, useRef } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import toast from 'react-hot-toast'

export default function ReportPage() {
  const params = useParams()
  const analysisId = params?.id as string
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('profile')
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
      pdf.save(`linkedin-brand-strategy-${new Date().toISOString().split('T')[0]}.pdf`)
      toast.success('PDF exported successfully!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-warm-ivory flex items-center justify-center font-manrope">
        <div className="text-center">
          <p className="text-dark-graphite animate-pulse font-medium">Assembling growth strategy report...</p>
        </div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-warm-ivory flex items-center justify-center font-manrope">
        <div className="text-center">
          <p className="text-dark-graphite font-medium mb-4">Report not found or has failed execution.</p>
          <Link href="/dashboard" className="btn-primary">Back to Dashboard</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-warm-ivory font-manrope">
      {/* Navigation */}
      <nav className="bg-white border-b border-soft-beige fixed top-0 w-full z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="font-space-grotesk text-2xl font-bold text-forest-green flex items-center gap-2">
            💼 LinkedIn Growth Agent
          </Link>
          <div className="flex gap-4">
            <button onClick={exportPDF} className="btn-secondary text-sm">
              Export PDF
            </button>
            <Link href="/dashboard" className="btn-primary text-sm">
              Back to Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-6 pt-28 pb-16">
        <div ref={reportRef} className="bg-white rounded-xl border border-soft-beige p-8 shadow-sm">
          {/* Report Header */}
          <div className="mb-8 pb-8 border-b border-soft-beige">
            <div className="flex justify-between items-start">
              <div>
                <span className="bg-muted-gold bg-opacity-20 text-forest-green text-xs font-bold px-2.5 py-1 rounded uppercase tracking-wider mb-3 inline-block">
                  Growth Strategy Report
                </span>
                <h1 className="text-4xl font-bold mb-2 font-space-grotesk text-forest-green">{report.profile_url}</h1>
                <p className="text-dark-graphite opacity-75">{report.industry}</p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-forest-green font-space-grotesk">{report.profile_score}%</div>
                <div className="text-xs text-dark-graphite opacity-50 uppercase tracking-wider font-bold">Optimization Score</div>
              </div>
            </div>
            <p className="text-xs text-dark-graphite opacity-40 mt-6">
              Generated on {new Date(report.created_at).toLocaleString()}
            </p>
          </div>

          {/* Quick Context Card */}
          <div className="bg-warm-ivory rounded-lg p-6 mb-8 border border-soft-beige grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-forest-green mb-2">Target Audience</h4>
              <p className="text-sm opacity-80">{report.target_audience}</p>
            </div>
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-forest-green mb-2">Career Goals</h4>
              <p className="text-sm opacity-80">{report.career_goals}</p>
            </div>
          </div>

          {/* Report Tabs */}
          <div className="flex border-b border-soft-beige mb-8 overflow-x-auto gap-2">
            {[
              { id: 'profile', label: '1. Profile Optimization' },
              { id: 'brand', label: '2. Brand Positioning' },
              { id: 'strategy', label: '3. Content Strategy' },
              { id: 'posts', label: '4. Generated Posts' },
              { id: 'roadmap', label: '5. Growth Roadmap' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-3 px-4 font-bold text-sm border-b-2 transition whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-forest-green text-forest-green font-space-grotesk'
                    : 'border-transparent text-dark-graphite opacity-50 hover:opacity-85'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="min-h-[400px]">
            {activeTab === 'profile' && report.profile_optimization && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-4 font-space-grotesk">Headline Suggestions</h3>
                  <div className="space-y-3">
                    {report.profile_optimization.headline_suggestions.map((headline: string, i: number) => (
                      <div key={i} className="bg-warm-ivory p-4 rounded-lg border border-soft-beige font-mono text-sm">
                        {headline}
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">"About" Section Rewrite</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige whitespace-pre-line text-sm leading-relaxed text-dark-graphite opacity-85">
                    {report.profile_optimization.about_improvements}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Experience Highlights Optimization</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige text-sm leading-relaxed text-dark-graphite opacity-85">
                    {report.profile_optimization.experience_optimization}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Keywords & Skills Recommendations</h3>
                  <div className="flex flex-wrap gap-2">
                    {report.profile_optimization.skills_recommendations.map((skill: string, idx: number) => (
                      <span key={idx} className="bg-forest-green bg-opacity-10 text-forest-green text-xs font-semibold px-3 py-1.5 rounded-full border border-forest-green border-opacity-20">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'brand' && report.personal_brand && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Brand Identity Label</h3>
                  <div className="text-2xl font-bold text-dark-graphite font-space-grotesk bg-warm-ivory p-4 rounded-lg border border-soft-beige inline-block">
                    🏷️ {report.personal_brand.brand_identity}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Elevator Positioning Statement</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige text-lg font-medium leading-relaxed italic text-dark-graphite">
                    "{report.personal_brand.positioning_statement}"
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Core Content Pillars</h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    {report.personal_brand.content_pillars.map((pillar: string, i: number) => (
                      <div key={i} className="card p-4 flex items-center justify-between border-forest-green border-opacity-30 bg-forest-green bg-opacity-5">
                        <span className="font-bold text-forest-green">{pillar}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Ideal Reader Profile</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige text-sm leading-relaxed text-dark-graphite opacity-85">
                    {report.personal_brand.audience_profile}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'strategy' && report.content_strategy && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-4 font-space-grotesk">Weekly Calendar</h3>
                  <div className="grid md:grid-cols-5 gap-4">
                    {report.content_strategy.weekly_calendar.map((item: any, i: number) => (
                      <div key={i} className="border border-soft-beige rounded-lg p-4 bg-warm-ivory flex flex-col justify-between">
                        <div>
                          <span className="font-bold text-xs uppercase tracking-wider text-forest-green block mb-2">{item.day}</span>
                          <span className="bg-forest-green bg-opacity-10 text-forest-green text-[10px] font-bold px-2 py-0.5 rounded-full block mb-3 text-center">
                            {item.pillar}
                          </span>
                          <p className="text-xs text-dark-graphite opacity-80 leading-relaxed">{item.post_concept}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">30-Day Monthly Strategy Focus</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige text-sm leading-relaxed text-dark-graphite opacity-85 whitespace-pre-line">
                    {report.content_strategy.monthly_strategy}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Strategy Themes</h3>
                  <ul className="list-disc list-inside space-y-2 text-sm text-dark-graphite opacity-85">
                    {report.content_strategy.content_themes.map((theme: string, i: number) => (
                      <li key={i}>{theme}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Viral Post Opportunities</h3>
                  <div className="bg-warm-ivory p-6 rounded-lg border border-soft-beige text-sm leading-relaxed text-dark-graphite opacity-85">
                    {report.content_strategy.viral_opportunities}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'posts' && report.post_generation && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-4 font-space-grotesk">Copy-Pasteable LinkedIn Posts</h3>
                  <div className="space-y-6">
                    {report.post_generation.posts.map((post: any) => (
                      <div key={post.post_id} className="border border-soft-beige rounded-xl p-6 bg-warm-ivory relative">
                        <div className="flex justify-between items-center mb-4 border-b border-soft-beige pb-3">
                          <span className="font-bold text-xs uppercase tracking-wider text-forest-green">Post {post.post_id} ({post.theme})</span>
                          <button
                            onClick={() => {
                              navigator.clipboard.writeText(`${post.hook}\n\n${post.body}\n\n${post.hashtags.join(' ')}`)
                              toast.success('Post copied to clipboard!')
                            }}
                            className="bg-forest-green text-warm-ivory text-xs px-2.5 py-1.5 rounded hover:bg-opacity-95 font-bold transition"
                          >
                            Copy Post Copy
                          </button>
                        </div>
                        <p className="text-base font-semibold mb-3 text-dark-graphite">{post.hook}</p>
                        <p className="text-sm whitespace-pre-line leading-relaxed text-dark-graphite opacity-85 mb-4">{post.body}</p>
                        <div className="flex gap-2">
                          {post.hashtags.map((tag: string, idx: number) => (
                            <span key={idx} className="text-xs font-semibold text-forest-green">{tag}</span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Alternative Creative Hooks</h3>
                  <div className="space-y-2">
                    {report.post_generation.hooks.map((hook: string, idx: number) => (
                      <div key={idx} className="bg-warm-ivory p-4 rounded-lg border border-soft-beige text-sm italic font-medium">
                        "{hook}"
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'roadmap' && report.growth_roadmap && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Days 1 - 30 Action Steps</h3>
                  <div className="bg-warm-ivory p-4 rounded-lg border border-soft-beige">
                    <ul className="list-decimal list-inside space-y-2 text-sm text-dark-graphite opacity-85">
                      {report.growth_roadmap.thirty_day_plan.map((task: string, i: number) => (
                        <li key={i}>{task}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Days 31 - 60 Action Steps</h3>
                  <div className="bg-warm-ivory p-4 rounded-lg border border-soft-beige">
                    <ul className="list-decimal list-inside space-y-2 text-sm text-dark-graphite opacity-85">
                      {report.growth_roadmap.sixty_day_plan.map((task: string, i: number) => (
                        <li key={i}>{task}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk">Days 61 - 90 Action Steps</h3>
                  <div className="bg-warm-ivory p-4 rounded-lg border border-soft-beige">
                    <ul className="list-decimal list-inside space-y-2 text-sm text-dark-graphite opacity-85">
                      {report.growth_roadmap.ninety_day_plan.map((task: string, i: number) => (
                        <li key={i}>{task}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-forest-green mb-3 font-space-grotesk font-space-grotesk">Success Milestones & KPIs</h3>
                  <div className="flex flex-wrap gap-3">
                    {report.growth_roadmap.milestones.map((milestone: string, idx: number) => (
                      <span key={idx} className="bg-muted-gold bg-opacity-25 text-dark-graphite text-xs font-bold px-4 py-2 rounded-lg border border-muted-gold">
                        ⭐ {milestone}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
