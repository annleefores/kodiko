"use client";
import { signIn, signOut, useSession } from "next-auth/react";
import user from "../../../public/user.png";
import logo from "../../../public/kodiko-logo.png";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import Image from "next/image";

const AuthButton = () => {
  const { data: session } = useSession();

  return (
    <div className="flex flex-row items-center">
      <div>
        {session ? (
          <Image
            className="rounded-full"
            src={session?.user?.image || user}
            width={35}
            height={35}
            alt="profile picture"
          />
        ) : (
          <div>Not signed in</div>
        )}
      </div>
      <div>
        {session ? (
          <button onClick={() => signOut()}>Sign Out</button>
        ) : (
          <button onClick={() => signIn()}>Sign In</button>
        )}
      </div>
    </div>
  );
};

export const NavMenu = () => {
  return (
    <div className="flex border-b p-1 px-3 w-full mt-2">
      <NavigationMenu>
        <NavigationMenuList>
          <div className="flex justify-between items-center w-full ">
            <div>
              <NavigationMenuItem>
                <Image
                  className="rounded-full"
                  src={logo}
                  width={35}
                  height={35}
                  alt="profile picture"
                />
              </NavigationMenuItem>
            </div>
            <div>
              <AuthButton />
            </div>
          </div>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  );
};
