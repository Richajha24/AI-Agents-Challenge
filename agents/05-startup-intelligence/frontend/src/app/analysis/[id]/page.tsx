import { AnalysisProgress } from "@/components/progress/AnalysisProgress";

export default async function AnalysisProgressPage({params}:{params:Promise<{id:string}>}) {
  return <AnalysisProgress reportId={(await params).id} />;
}
