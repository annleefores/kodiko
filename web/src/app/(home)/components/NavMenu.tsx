import logo from "../../../../public/kodiko-logo.png";
import Image from "next/image";
import Link from "next/link";
import AuthButton from "./AuthButton";

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
