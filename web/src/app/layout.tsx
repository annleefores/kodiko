import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "@/components/ui/toaster";

import SessionProvider from "./(home)/components/SessionProvider";
import { getServerSession } from "next-auth";
import { NavMenu } from "./(home)/components/NavMenu";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Kodiko",
  description: "A super simple cloud IDE",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession();

  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider session={session}>
          <div className="h-full w-full">
            <NavMenu />
            {children}
            <Toaster />
          </div>
        </SessionProvider>
      </body>
    </html>
  );
}
