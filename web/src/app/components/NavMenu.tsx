"use client";
import { signIn, signOut, useSession } from "next-auth/react";
import user from "../../../public/user.png";
import logo from "../../../public/kodiko-logo.png";

import Image from "next/image";
import Link from "next/link";

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

export const NavMenu = () => {
  return (
    <div className="flex items-center border-b py-2.5 px-4 w-full">
      <div className="flex justify-between  w-full ">
        <div>
          <Link href="/">
            <Image
              className="rounded-full"
              src={logo}
              width={26}
              height={26}
              alt="profile picture"
            />
          </Link>
        </div>
        <div>
          <AuthButton />
        </div>
      </div>
    </div>
  );
};
