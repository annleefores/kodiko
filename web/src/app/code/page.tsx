"use client";
import dynamic from "next/dynamic";
const Xterm = dynamic(() => import("./components/Xterm"), { ssr: false });

const Home = () => {
  return (
    <>
      <div className="flex h-full w-full">
        <Xterm />
      </div>
    </>
  );
};

export default Home;
