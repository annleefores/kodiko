import dynamic from "next/dynamic";
const Xterm = dynamic(() => import("./components/Xterm"), { ssr: false });
import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";

const Home = async () => {
  const session = await getServerSession();

  if (!session || !session.user) {
    redirect("/");
  }

  return (
    <>
      <div className="flex h-full w-full">
        <Xterm />
      </div>
    </>
  );
};

export default Home;
