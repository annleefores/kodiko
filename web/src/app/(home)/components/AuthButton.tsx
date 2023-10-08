"use client";
import Image from "next/image";
import React from "react";
import { signIn, signOut, useSession } from "next-auth/react";
import user from "../../../../public/user.png";

const AuthButton = () => {
  const { data: session } = useSession();

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
            onClick={() => signIn("github")}
            className="text-sm transition ease-in-out delay-130 hover:text-neutral-300"
          >
            Sign in with GitHub
          </button>
        )}
      </div>
    </div>
  );
};

export default AuthButton;
