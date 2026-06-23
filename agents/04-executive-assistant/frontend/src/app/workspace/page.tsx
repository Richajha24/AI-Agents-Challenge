"use client";

import { useEffect, useMemo, useState } from "react";
import { startWorkspaceReport, getWorkspaceReport } from "@/lib/api";

type WorkspaceReportState = {
    report_id?: string;
    status?: string;
    progress?: number;
    goals?: string | null;
    priority_analysis?: any;
    meeting_briefs?: any;
};

function uniqNonEmpty(lines: string[]) {
    return lines.map((l) => l.trim()).filter(Boolean);
}

export default function WorkspacePage() {
    const [goals, setGoals] = useState<string>("");
    const [tasksRaw, setTasksRaw] = useState<string>("Review marketing materials\nBug fix in payment gateway");
    const [meetingsRaw, setMeetingsRaw] = useState<string>("Product alignment with CTO|CTO, Lead Designer|CTO sync");

    const [report, setReport] = useState<WorkspaceReportState | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const tasks_input = useMemo(() => {
        const lines = uniqNonEmpty(tasksRaw.split("\n"));
        return lines.map((t) => ({ title: t, description: null, deadline: null, category: null }));
    }, [tasksRaw]);

    const meetings_input = useMemo(() => {
        const lines = uniqNonEmpty(meetingsRaw.split("\n"));
        return lines.map((line) => {
            const [topic, participants, notes] = line.split("|").map((s) => (s ?? "").trim());
            return {
                topic: topic || "Meeting",
                participants: participants || null,
                time: null,
                notes: notes || null
            };
        });
    }, [meetingsRaw]);

    async function onGenerate() {
        setError(null);
        setLoading(true);
        try {
            const res = await startWorkspaceReport({
                goals: goals || null,
                tasks_input,
                meetings_input
            });

            setReport({ report_id: res.report_id, status: res.status, progress: 0 });

            // Poll until completed/failed
            let done = false;
            while (!done) {
                await new Promise((r) => setTimeout(r, 1200));
                const next = await getWorkspaceReport(res.report_id);
                setReport((prev) => ({
                    ...(prev || {}),
                    report_id: next.report_id,
                    status: next.status,
                    progress: next.progress,
                    goals: next.goals,
                    priority_analysis: next.priority_analysis,
                    meeting_briefs: next.meeting_briefs
                }));
                if (next.status === "completed" || next.status === "failed") {
                    done = true;
                }
            }
        } catch (e: any) {
            setError(e?.message || "Failed to generate workspace report");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="min-h-screen p-6">
            <div className="mx-auto w-full max-w-5xl">
                <div className="card rounded-2xl p-6">
                    <h1 className="text-xl font-semibold">Workspace Report</h1>
                    <p className="mt-1 text-sm text-white/70">Generate prioritized tasks + meeting briefs in one run.</p>

                    <div className="mt-6 grid gap-4 md:grid-cols-2">
                        <label className="block">
                            <span className="text-sm text-white/80">Goals</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={3}
                                value={goals}
                                onChange={(e) => setGoals(e.target.value)}
                                placeholder="e.g. Launch beta version by Friday"
                            />
                        </label>

                        <div className="rounded-2xl border border-gold/20 bg-graphite/30 p-4">
                            <div className="text-sm text-white/80">Quick input format</div>
                            <ul className="mt-2 list-disc pl-5 text-xs text-white/70">
                                <li>Tasks: one per line</li>
                                <li>Meetings: topic|participants|notes (one per line)</li>
                            </ul>
                        </div>

                        <label className="block md:col-span-2">
                            <span className="text-sm text-white/80">Tasks</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={5}
                                value={tasksRaw}
                                onChange={(e) => setTasksRaw(e.target.value)}
                            />
                        </label>

                        <label className="block md:col-span-2">
                            <span className="text-sm text-white/80">Meetings</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={4}
                                value={meetingsRaw}
                                onChange={(e) => setMeetingsRaw(e.target.value)}
                            />
                        </label>
                    </div>

                    <div className="mt-6 flex items-center gap-3">
                        <button
                            onClick={onGenerate}
                            disabled={loading}
                            className="rounded-xl bg-gold/20 px-4 py-2 text-sm font-semibold text-ivory ring-1 ring-gold/40 hover:bg-gold/30 disabled:opacity-50"
                        >
                            {loading ? "Generating..." : "Generate Report"}
                        </button>

                        {report?.status ? (
                            <div className="text-sm text-white/70">
                                Status: <span className="text-white/90">{report.status}</span>
                                {typeof report.progress === "number" ? (
                                    <span> · {report.progress}%</span>
                                ) : null}
                            </div>
                        ) : null}
                    </div>

                    {error ? <div className="mt-4 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-sm">{error}</div> : null}
                </div>

                {report?.status === "completed" ? (
                    <div className="mt-6 grid gap-4 md:grid-cols-2">
                        <section className="card rounded-2xl p-6">
                            <h2 className="text-lg font-semibold">Priority Analysis</h2>
                            <pre className="mt-3 whitespace-pre-wrap text-xs text-white/75">{JSON.stringify(report.priority_analysis, null, 2)}</pre>
                        </section>

                        <section className="card rounded-2xl p-6">
                            <h2 className="text-lg font-semibold">Meeting Briefs</h2>
                            <pre className="mt-3 whitespace-pre-wrap text-xs text-white/75">{JSON.stringify(report.meeting_briefs, null, 2)}</pre>
                        </section>
                    </div>
                ) : null}
            </div>
        </main>
    );
}


