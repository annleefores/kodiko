import Image from 'next/image'
import logo from '../../../public/assets/kodiko-logo-text.png'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
     <Image
              src={logo}
              alt="Kodiko Logo"
              width={300}
              priority
            /> 
    </main>
  )
}
