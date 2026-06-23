"use client";

import { useState } from "react";
import { prepareMeeting } from "@/lib/api";

export default function MeetingsPage() {
    const [topic, setTopic] = useState<string>("Product alignment with CTO");
    const [participants, setParticipants] = useState<string>("CTO, Lead Designer");
    const [context, setContext] = useState<string>("Aligning design system changes and release timelines for payment gateway update.");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<any | null>(null);

    async function onPrepare() {
        setLoading(true);
        setError(null);
        try {
            const res = await prepareMeeting({ topic, participants, context });
            setResult(res);
        } catch (e: any) {
            setError(e?.message || "Failed to prepare meeting");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="min-h-screen p-6">
            <div className="mx-auto w-full max-w-5xl">
                <div className="card rounded-2xl p-6">
                    <h1 className="text-xl font-semibold">Meeting Preparation</h1>
                    <p className="mt-1 text-sm text-white/70">Generate agenda, discussion points, and risk areas.</p>

                    <div className="mt-6 grid gap-4 md:grid-cols-2">
                        <label className="block md:col-span-2">
                            <span className="text-sm text-white/80">Topic</span>
                            <input
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                            />
                        </label>

                        <label className="block">
                            <span className="text-sm text-white/80">Participants</span>
                            <input
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                value={participants}
                                onChange={(e) => setParticipants(e.target.value)}
                            />
                        </label>

                        <label className="block">
                            <span className="text-sm text-white/80">Context (notes)</span>
                            <textarea
                                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                                rows={4}
                                value={context}
                                onChange={(e) => setContext(e.target.value)}
                            />
                        </label>
                    </div>

                    <div className="mt-6 flex items-center gap-3">
                        <button
                            onClick={onPrepare}
                            disabled={loading}
                            className="rounded-xl bg-gold/20 px-4 py-2 text-sm font-semibold text-ivory ring-1 ring-gold/40 hover:bg-gold/30 disabled:opacity-50"
                        >
                            {loading ? "Preparing..." : "Prepare Meeting"}
                        </button>
                    </div>

                    {error ? <div className="mt-4 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-sm">{error}</div> : null}
                </div>

                {result ? (
                    <section className="mt-6 card rounded-2xl p-6">
                        <h2 className="text-lg font-semibold">Brief</h2>
                        <pre className="mt-3 whitespace-pre-wrap text-xs text-white/75">{result?.brief}</pre>

                        <div className="mt-5 grid gap-4 md:grid-cols-2">
                            <div>
                                <h3 className="text-sm font-semibold text-ivory">Agenda</h3>
                                <ul className="mt-2 list-disc pl-5 text-xs text-white/75">
                                    {(result?.agenda || []).map((a: string, idx: number) => (
                                        <li key={idx}>{a}</li>
                                    ))}
                                </ul>
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold text-ivory">Discussion Points</h3>
                                <ul className="mt-2 list-disc pl-5 text-xs text-white/75">
                                    {(result?.discussion_points || []).map((a: string, idx: number) => (
                                        <li key={idx}>{a}</li>
                                    ))}
                                </ul>
                            </div>

                            <div className="md:col-span-2">
                                <h3 className="text-sm font-semibold text-ivory">Risk Areas</h3>
                                <ul className="mt-2 list-disc pl-5 text-xs text-white/75">
                                    {(result?.risk_areas || []).map((a: string, idx: number) => (
                                        <li key={idx}>{a}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </section>
                ) : null}
            </div>
        </main>
    );
}


