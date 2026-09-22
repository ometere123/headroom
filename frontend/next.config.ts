import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  reactStrictMode: true,
  turbopack: { root: process.cwd() },
  async redirects() {
    return [
      { source: "/covenants", destination: "/services", permanent: false },
      { source: "/open", destination: "/services/new", permanent: false },
      { source: "/account", destination: "/settlements", permanent: false },
    ];
  },
};
export default nextConfig;

