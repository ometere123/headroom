import {ImageResponse} from "next/og";
export const size={width:64,height:64};export const contentType="image/png";
export default function Icon(){return new ImageResponse(<div style={{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center",background:"#090b0d"}}><svg width="60" height="60" viewBox="0 0 64 64"><path d="M5 5h39l15 15v39H20L5 44z" fill="#0a0d0f" stroke="#c7ff4a" strokeWidth="3"/><path d="M18 18h25l7 7v21H25l-7-7z" fill="none" stroke="#ff6b2c" strokeWidth="3"/><path d="M24 29h18M24 36h13" stroke="#9ddcff" strokeWidth="2"/></svg></div>,size)}
