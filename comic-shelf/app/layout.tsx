import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'Panel — Your Marvel comic shelf',
  description:
    'Explore Marvel comics in your Orange County Library System catalog.',
};
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
