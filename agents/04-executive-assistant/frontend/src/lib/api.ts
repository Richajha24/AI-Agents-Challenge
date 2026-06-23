const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function parseJsonSafe<T>(res: Response): Promise<T> {
    const text = await res.text();
    if (!text) return {} as T;
    try {
        return JSON.parse(text) as T;
    } catch {
        return text as unknown as T;
    }
}

export async function startWorkspaceReport(payload: {
    goals?: string;
    tasks_input: Array<any>;
    meetings_input: Array<any>;
}): Promise<{ report_id: string; status: string; message?: string }> {
    const res = await fetch(`${API_BASE_URL}/api/report/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to start report (${res.status})`);
    }

    return (await parseJsonSafe<any>(res)) as any;
}

export async function getWorkspaceReport(reportId: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/api/report/${encodeURIComponent(reportId)}`);
    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to fetch report (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any;
}

export async function getReportHistory(limit = 20): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/api/report/history?limit=${encodeURIComponent(String(limit))}`);
    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to fetch report history (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any[];
}

export async function analyzeTasks(payload: { tasks: Array<any>; goals?: string }) {
    const res = await fetch(`${API_BASE_URL}/api/tasks/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to analyze tasks (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any;
}

export async function prepareMeeting(payload: { topic: string; participants?: string; context?: string }) {
    const res = await fetch(`${API_BASE_URL}/api/meetings/prepare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to prepare meeting (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any;
}

export async function analyzeDecision(payload: { problem_statement: string; options: string[] }) {
    const res = await fetch(`${API_BASE_URL}/api/decisions/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to analyze decision (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any;
}

export async function getDecisionHistory(limit = 20): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/api/decisions/history?limit=${encodeURIComponent(String(limit))}`);
    if (!res.ok) {
        const err = await parseJsonSafe<any>(res);
        throw new Error(err?.detail || `Failed to fetch decision history (${res.status})`);
    }
    return (await parseJsonSafe<any>(res)) as any[];
}

