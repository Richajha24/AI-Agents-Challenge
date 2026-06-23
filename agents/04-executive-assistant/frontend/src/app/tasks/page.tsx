"use client";

import { useMemo, useState } from "react";
import { analyzeTasks } from "@/lib/api";

export default function TasksPage() {
  const [goals, setGoals] = useState<string>("Launch beta version by Friday");
  const [tasksRaw, setTasksRaw] = useState<string>(
    "Review marketing materials\nBug fix in payment gateway"
  );

  const tasks_input = useMemo(() => {
    return tasksRaw
      .split("\n")
      .map((t) => t.trim())
      .filter(Boolean)
      .map((t) => ({ title: t, description: null, deadline: null, category: null }));
  }, [tasksRaw]);

  const [result, setResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onAnalyze() {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeTasks({ tasks: tasks_input, goals: goals || undefined });
      setResult(res);
    } catch (e: any) {
      setError(e?.message || "Failed to analyze tasks");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto w-full max-w-5xl">
        <div className="card rounded-2xl p-6">
          <h1 className="text-xl font-semibold">Priority Tasks</h1>
          <p className="mt-1 text-sm text-white/70">Rank tasks, suggest focus, and build critical path.</p>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <label className="block md:col-span-2">
              <span className="text-sm text-white/80">Goals</span>
              <textarea
                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                rows={3}
                value={goals}
                onChange={(e) => setGoals(e.target.value)}
              />
            </label>

            <label className="block md:col-span-2">
              <span className="text-sm text-white/80">Tasks (one per line)</span>
              <textarea
                className="mt-2 w-full rounded-xl border border-gold/30 bg-graphite/40 p-3 text-sm outline-none focus:border-gold/60"
                rows={7}
                value={tasksRaw}
                onChange={(e) => setTasksRaw(e.target.value)}
              />
            </label>
          </div>

          <div className="mt-5 flex items-center gap-3">
            <button
              onClick={onAnalyze}
              disabled={loading}
              className="rounded-xl bg-gold/20 px-4 py-2 text-sm font-semibold text-ivory ring-1 ring-gold/40 hover:bg-gold/30 disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
            {result?.critical_path ? (
              <div className="text-sm text-white/70">
                Critical Path: <span className="text-white/90">{JSON.stringify(result.critical_path)}</span>
              </div>
            ) : null}
          </div>

          {error ? (
            <div className="mt-4 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-sm">{error}</div>
          ) : null}
        </div>

        {result ? (
          <section className="mt-6 card rounded-2xl p-6">
            <h2 className="text-lg font-semibold">Result</h2>
            <pre className="mt-3 whitespace-pre-wrap text-xs text-white/75">{JSON.stringify(result, null, 2)}</pre>
          </section>
        ) : null}
      </div>
    </main>
  );
}


