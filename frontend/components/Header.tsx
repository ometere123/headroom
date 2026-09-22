"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { WalletButton } from "./WalletButton";
import { TimeZoneControl } from "./ContractDateTime";
import { CONTRACT_ADDRESS, EXPLORER } from "@/lib/config";

const items = [
  ["/control", "Control", "01"], ["/services", "Services", "02"],
  ["/admissions", "Admissions", "03"], ["/changes", "Change Control", "04"],
  ["/Incidents", "Incidents", "05"], ["/settlements", "Settlements", "06"],
];
export function Header() {
  const path = usePathname();
  if (path === "/") return <header className="landing-head"><Link className="brand" href="/"><img src="/headroom-mark.svg" alt=""/><b>HEADROOM</b></Link><span className="network-tag">GENLAYER STUDIONET · 61999</span><Link className="button ghost" href="/control">Enter Control Room</Link></header>;
  const app = path.startsWith("/control") || path.startsWith("/services") || path.startsWith("/admissions") || path.startsWith("/changes") || path.startsWith("/Incidents") || path.startsWith("/settlements") || path.startsWith("/protocol") || path.startsWith("/covenants") || path.startsWith("/open") || path.startsWith("/account");
  if (!app) return null;
  return <><div className="status-strip"><Link className="compact-brand" href="/control"><img src="/headroom-mark.svg" alt=""/><b>HEADROOM</b></Link><span className="live-led">GENLAYER STUDIONET</span><span>CHAIN 61999</span><a href={CONTRACT_ADDRESS ? `${EXPLORER}/address/${CONTRACT_ADDRESS}` : undefined}>CONTRACT {CONTRACT_ADDRESS ? `${CONTRACT_ADDRESS.slice(0, 7)}…${CONTRACT_ADDRESS.slice(-4)}` : "NOT CONFIGURED"}</a><TimeZoneControl/><WalletButton/></div><aside className="ops-rail"><div className="rail-caption">Operations</div>{items.map(([href,label,num])=><Link className={path===href || (href!=="/control"&&path.startsWith(href+"/")) ? "selected" : ""} href={href} key={href}><small>{num}</small><span>{label}</span></Link>)}<div className="rail-spacer"/><Link href="/protocol"><small>↗</small><span>Protocol</span></Link><Link href="/"><small>⌂</small><span>Product</span></Link></aside></>;
}
