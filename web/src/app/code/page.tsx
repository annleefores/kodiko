'use client'
import dynamic from 'next/dynamic'
const Xterm = dynamic(() => import('./components/Xterm'), { ssr: false })

const Home = () => {
    return (
        <>
            <div className="flex justify-center items-center h-full w-full bg-white">
                <Xterm />
            </div>
        </>
    );
};

export default Home;