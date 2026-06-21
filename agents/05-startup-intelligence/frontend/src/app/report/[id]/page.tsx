import { ResearchReport } from "@/components/reports/ResearchReport";

export default async function ReportPage({params}:{params:Promise<{id:string}>}) {
  return <ResearchReport reportId={(await params).id} />;
}
