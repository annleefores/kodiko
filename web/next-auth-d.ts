import { JWT } from "next-auth/jwt";
import { Session, User } from "next-auth";

declare module "next-auth" {
  interface Session {
    accessToken?: string;
    idToken?: string;
    error?: string;
  }
}
declare module "next-auth" {
  interface User {
    picture?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    idToken?: string;
    refreshToken: string;
    expiresAt: number;
    tokenType: string;
    error?: string;
  }
}
