"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import {
  signIn,
  signOut,
  useSession,
  getProviders,
  LiteralUnion,
  ClientSafeProvider,
} from "next-auth/react";
import user from "../../../../public/user.png";
import { BuiltInProviderType } from "next-auth/providers/index";

const AuthButton = () => {
  const { data: session } = useSession();
  // state to hold custom providers
  const [providers, setProviders] = useState<Record<
    LiteralUnion<BuiltInProviderType, string>,
    ClientSafeProvider
  > | null>(null);

  // Fetch providers on mount.
  useEffect(() => {
    getProviders().then((providers) => setProviders(providers));
  }, []);

  console.log(session);

  return (
    <div className="flex flex-row gap-x-2 items-center">
      <div>
        {session ? (
          <Image
            className="rounded-full"
            src={session?.user?.image || user}
            width={26}
            height={26}
            alt="profile picture"
          />
        ) : (
          <></>
        )}
      </div>
      <div>
        {session ? (
          <button
            onClick={() => signOut()}
            className="text-sm transition ease-in-out delay-130 hover:text-neutral-300"
          >
            Sign Out
          </button>
        ) : (
          <button
            onClick={() => {
              if (providers) {
                signIn(providers["cognito_google"].id);
              }
            }}
            className="text-sm transition ease-in-out delay-130 hover:text-neutral-300"
          >
            Sign in with Google
          </button>
        )}
      </div>
    </div>
  );
};

export default AuthButton;
