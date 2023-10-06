import NextAuth from "next-auth";
import GithubProvider from "next-auth/providers/github";
import type { NextAuthOptions } from "next-auth";
import { z } from "zod";

const envSchema = z.object({
  GITHUB_ID: z.string().nonempty(),
  GITHUB_SECRET: z.string().nonempty(),
});

const result = envSchema.safeParse(process.env);

if (!result.success) {
  console.error(result.error);
  throw new Error("Invalid environment variables");
}

const config = result.data;
const authOptions: NextAuthOptions = {
  // Configure one or more authentication providers
  providers: [
    GithubProvider({
      clientId: config.GITHUB_ID,
      clientSecret: config.GITHUB_SECRET,
    }),
    // ...add more providers here
  ],
  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
