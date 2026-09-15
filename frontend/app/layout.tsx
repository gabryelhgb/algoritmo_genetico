import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Laboratório Evolutivo | Algoritmo Genético",
  description: "Visualização interativa de um algoritmo genético para maximização de função.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="pt-BR"><body>{children}</body></html>;
}
