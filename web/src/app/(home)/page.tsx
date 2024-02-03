import Image from "next/image";
import logo from "../../../public/kodiko-logo-text.png";
import CreateDeleteButton from "./components/CreateDeleteButton";
import { getServerSession } from "next-auth";
import LaunchingSoon from "./components/LaunchingSoon";

export default async function Home() {
  const session = await getServerSession();

  // temporary feature flag
  const enable_button =
    process.env.NEXT_PUBLIC_ENABLE_BUTTON === "true" || false;

  return (
    <main className="flex flex-col items-center gap-y-16 mt-16">
      <div className="flex flex-col justify-center items-center gap-y-6">
        <div>
          <Image src={logo} alt="Kodiko Logos" width={300} priority />
        </div>
        <div>
          <p className="font-semibold text-lg text-neutral-200">
            A super simple Cloud IDE
          </p>
        </div>
      </div>
      {session && enable_button ? <CreateDeleteButton /> : <></>}
      {enable_button ? <></> : <LaunchingSoon />}
    </main>
  );
}
