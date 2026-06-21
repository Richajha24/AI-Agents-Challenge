import type { ReactNode } from "react";

import "./globals.css";
import { Manrope, Space_Grotesk } from "next/font/google";

const manrope = Manrope({ subsets: ["latin"], variable: "--font-manrope" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space" });

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body className={`${manrope.variable} ${spaceGrotesk.variable}`}>{children}</body></html>;
}
