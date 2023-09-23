import Image from "next/image";
import logo from "../../../public/kodiko-logo-text.png";
import CreateDeleteButton from "./components/CreateDeleteButton";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-y-16  p-24">
      <Image src={logo} alt="Kodiko Logos" width={300} priority />
      <CreateDeleteButton />
    </main>
  );
}
