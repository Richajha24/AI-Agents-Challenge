export type AnalysisStatus = "pending" | "processing" | "completed" | "failed";

export type AnalysisType = "market" | "competitor" | "trend" | "swot";

export interface AnalysisResponse {
  id: string;
  analysis_type: AnalysisType;
  status: AnalysisStatus;
  progress: number;
  results: Record<string, unknown> | null;
  report_id: string | null;
  error_message: string | null;
}

export interface Report {
  id: string;
  analysis_id: string;
  report_type: AnalysisType;
  content: { analysis_type: string; input: Record<string, unknown>; findings: Record<string, unknown>; generated_at: string };
  created_at: string;
}
