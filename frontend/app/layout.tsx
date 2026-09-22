import "./globals.css";
import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
export const metadata:Metadata={title:{default:"HEADROOM - Preventive SLA Admission & Enforcement",template:"%s Â· HEADROOM"},description:"A preventive SLA protocol: deterministic headroom gates and GenLayer consensus control commitments before risk, then govern incident facts before deterministic settlement.",metadataBase:new URL("https://the-headroom.vercel.app"),openGraph:{title:"HEADROOM - Donâ€™t Promise What You Canâ€™t Serve",description:"Consensus before risk. Consensus after failure.",url:"https://the-headroom.vercel.app",siteName:"HEADROOM",images:["/headroom-mark.svg"],type:"website"},icons:{icon:"/headroom-mark.svg"}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body><Header/><main>{children}</main><Footer/></body></html>}


