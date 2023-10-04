import Image from "next/image";
import logo from "../../../public/kodiko-logo-text.png";
import CreateDeleteButton from "./components/CreateDeleteButton";

export default function Home() {
  return (
    <main className="flex flex-col items-center gap-y-16 mt-16">
      <Image src={logo} alt="Kodiko Logos" width={300} priority />
      <CreateDeleteButton />
    </main>
  );
}
